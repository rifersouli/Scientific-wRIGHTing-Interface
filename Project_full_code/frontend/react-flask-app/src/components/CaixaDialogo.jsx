import React, { useState, useEffect, useRef } from 'react'
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';
import DialogTitle from '@mui/joy/DialogTitle';
import DialogContent from '@mui/joy/DialogContent';
import Button from '@mui/joy/Button';
import Typography from '@mui/joy/Typography';
import Box from '@mui/joy/Box';
import Chip from '@mui/joy/Chip';
import axios from 'axios';
import './CaixaDialogo.css';

const CaixaDialogo = ({ open = false, onClose, resumo }) => {
    const [currentStep, setCurrentStep] = useState('objetivo'); // 'objetivo', 'conclusao', 'complete'
    const [objetivoData, setObjetivoData] = useState(null);
    const [conclusaoData, setConclusaoData] = useState(null);
    const [selectedSentences, setSelectedSentences] = useState([]); // Array of selected sentence indices
    const [selectedNone, setSelectedNone] = useState(false);
    const [matchResult, setMatchResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [hasAttemptedLoad, setHasAttemptedLoad] = useState(false);
    
    // Refs for request cancellation
    const abortControllerRef = useRef(null);
    const currentRequestRef = useRef(null);

    // Reset state when modal opens/closes
    useEffect(() => {
        if (open) {
            setCurrentStep('objetivo');
            setObjetivoData(null);
            setConclusaoData(null);
            setSelectedSentences([]);
            setSelectedNone(false);
            setMatchResult(null);
            setLoading(false); // Reset loading state when opening modal
            setHasAttemptedLoad(false); // Reset attempt tracking when opening modal
            
            // Cancel any pending requests when opening modal
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        } else {
            // Reset all state when closing modal
            setCurrentStep('objetivo');
            setObjetivoData(null);
            setConclusaoData(null);
            setSelectedSentences([]);
            setSelectedNone(false);
            setMatchResult(null);
            setLoading(false); // Reset loading state when closing modal
            setHasAttemptedLoad(false); // Reset attempt tracking when closing modal
            
            // Cancel any pending requests when closing modal
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        }
    }, [open]);

    const loadAnalysisData = async (type) => {
        // Cancel any existing request
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
        }
        
        // Create new abort controller for this request
        abortControllerRef.current = new AbortController();
        const signal = abortControllerRef.current.signal;
        
        setLoading(true);
        setHasAttemptedLoad(true);
        try {
            const response = await axios.get(`http://localhost:5000/api/analysis/${type}/${resumo.id}`, {
                signal,
                timeout: 10000 // 10 second timeout
            });
            
            // Check if request was aborted
            if (signal.aborted) {
                return;
            }
            
            if (type === 'objetivo') {
                setObjetivoData(response.data);
            } else {
                setConclusaoData(response.data);
            }
        } catch (error) {
            // Don't show error if request was aborted
            if (error.name !== 'AbortError' && error.name !== 'CanceledError') {
                console.error('Error fetching analysis data:', error);
            }
        } finally {
            // Only set loading to false if request wasn't aborted
            if (!signal.aborted) {
                setLoading(false);
            }
        }
    };

    // Load objetivo data when component mounts
    useEffect(() => {
        if (open && currentStep === 'objetivo' && !objetivoData) {
            // Small delay to ensure modal is fully opened and state is reset
            const timer = setTimeout(() => {
                loadAnalysisData('objetivo');
            }, 100);
            return () => clearTimeout(timer);
        }
    }, [open, currentStep]);

    // Load conclusao data when moving to conclusao step
    useEffect(() => {
        if (currentStep === 'conclusao' && !conclusaoData) {
            loadAnalysisData('conclusao');
        }
    }, [currentStep]);

    // Cleanup effect to cancel requests when component unmounts
    useEffect(() => {
        return () => {
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
        };
    }, []);

    // Auto-scroll to result when it appears (for smaller screens)
    useEffect(() => {
        if (matchResult) {
            // Small delay to ensure the result element is rendered
            setTimeout(() => {
                const resultElement = document.querySelector('.result-box');
                if (resultElement) {
                    resultElement.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'center' 
                    });
                }
            }, 100);
        }
    }, [matchResult]);

    const handleSentenceSelect = (index) => {
        setSelectedSentences(prev => {
            if (prev.includes(index)) {
                // Remove if already selected
                return prev.filter(i => i !== index);
            } else {
                // Add if not selected
                return [...prev, index];
            }
        });
        setSelectedNone(false);
        setMatchResult(null);
    };

    const handleNoneSelect = () => {
        setSelectedNone(true);
        setSelectedSentences([]);
        setMatchResult(null);
    };

    const handleCheckMatch = async () => {
        const currentData = currentStep === 'objetivo' ? objetivoData : conclusaoData;
        if ((selectedSentences.length === 0 && !selectedNone) || !currentData) return;

        setLoading(true);
        try {
            if (selectedNone) {
                // Check if there's actually no objective/conclusion (empty annotated phrase)
                const hasAnnotatedPhrase = currentData.annotated_phrase && currentData.annotated_phrase.trim() !== '';
                setMatchResult({
                    match: !hasAnnotatedPhrase,
                    user_phrase: "Nenhuma das opções",
                    annotated_phrase: hasAnnotatedPhrase ? currentData.annotated_phrase : "Nenhuma frase anotada",
                    phrase_type: currentStep
                });
            } else {
                // Handle sentence selection with precise verification
                const annotatedPhrase = currentData.annotated_phrase || '';
                
                // Find sentences marked in the abstract text itself
                const markedSentences = findMarkedSentences(resumo?.resumo, currentStep);
                

                //DEBUGGING OPTIONS:
                // console.log('Verification Debug:', {
                //     markedSentences,
                //     selectedSentences,
                //     abstractText: resumo?.resumo?.substring(0, 200) + '...',
                //     stepType: currentStep,
                //     markers: currentStep === 'objetivo' ? ['--{', '}--'] : ['--[', ']--'],
                //     hasMarkers: resumo?.resumo?.includes(currentStep === 'objetivo' ? '--{' : '--[')
                // });
                
                // Check if user selected EXACTLY the marked sentences
                const hasAllMarked = markedSentences.every(index => selectedSentences.includes(index));
                const hasOnlyMarked = selectedSentences.every(index => markedSentences.includes(index));
                const hasCorrectCount = selectedSentences.length === markedSentences.length;
                const isExactMatch = hasAllMarked && hasOnlyMarked && hasCorrectCount && markedSentences.length > 0;
                
                // Always use precise verification logic
                setMatchResult({
                    match: isExactMatch,
                    user_phrase: selectedSentences.map(index => currentData.sentences[index]).join(' '),
                    annotated_phrase: annotatedPhrase,
                    phrase_type: currentStep,
                    required_sentences: markedSentences
                });
            }
        } catch (error) {
            console.error('Error checking match:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleNextStep = () => {
        if (currentStep === 'objetivo') {
            setCurrentStep('conclusao');
            setSelectedSentences([]);
            setSelectedNone(false);
            setMatchResult(null);
        } else if (currentStep === 'conclusao') {
            setCurrentStep('complete');
        }
    };

    // Function to find sentences marked with objective/conclusion markers in the abstract
    const findMarkedSentences = (abstractText, stepType) => {
        if (!abstractText) return [];
        
        const markers = stepType === 'objetivo' ? ['--{', '}--'] : ['--[', ']--'];
        const startMarker = markers[0];
        const endMarker = markers[1];
        
        //DEBUGGING OPTIONS:
        // console.log('Finding marked sentences:', { stepType, startMarker, endMarker });
        
        // First, remove all markers to get clean text for sentence splitting
        let cleanText = abstractText;
        cleanText = cleanText.replace(/--\{/g, '').replace(/\}--/g, '');
        cleanText = cleanText.replace(/--\[/g, '').replace(/\]--/g, '');
        
        // Split into sentences (split by punctuation)
        const allSentences = cleanText.split(/[.!?]+/).map(s => s.trim()).filter(s => s.length > 0);
        
        //DEBUGGING OPTIONS:
        // console.log('All sentences (clean):', allSentences);
        
        const markedSentences = [];
        let startIndex = 0;
        
        // Find all marked sections in original text
        while (true) {
            const startPos = abstractText.indexOf(startMarker, startIndex);
            if (startPos === -1) break;
            
            const endPos = abstractText.indexOf(endMarker, startPos);
            if (endPos === -1) break;
            
            const markedText = abstractText.substring(startPos + startMarker.length, endPos).trim();
            
            //DEBUGGING OPTIONS:
            // console.log('Found marked text:', markedText);
            
            // Find which sentence contains this marked text
            allSentences.forEach((sentence, index) => {
                const cleanSentence = sentence.trim();
                // Check if the marked text is contained in this sentence
                if (cleanSentence && markedText.includes(cleanSentence)) {
                    
                    //DEBUGGING OPTIONS:
                    // console.log(`Sentence ${index} matches: "${cleanSentence}"`);
                    
                    markedSentences.push(index);
                }
            });
            
            startIndex = endPos + endMarker.length;
        }
        
        
        //DEBUGGING OPTIONS:
        // console.log('Final marked sentences:', [...new Set(markedSentences)]);
        
        return [...new Set(markedSentences)]; // Remove duplicates
    };

    // Function to parse and highlight abstract text
    const renderHighlightedAbstract = (abstractText) => {
        if (!abstractText) return null;

        // Parse the text and create highlighted segments
        const segments = [];
        let currentIndex = 0;
        let segmentIndex = 0;

        // Find all markers and their positions
        const markers = [];
        const objectiveRegex = /--\{([^}]+)\}--/g;
        const conclusionRegex = /--\[([^\]]+)\]--/g;

        let match;
        while ((match = objectiveRegex.exec(abstractText)) !== null) {
            markers.push({
                type: 'objective',
                start: match.index,
                end: match.index + match[0].length,
                content: match[1],
                fullMatch: match[0]
            });
        }

        while ((match = conclusionRegex.exec(abstractText)) !== null) {
            markers.push({
                type: 'conclusion',
                start: match.index,
                end: match.index + match[0].length,
                content: match[1],
                fullMatch: match[0]
            });
        }

        // Sort markers by position
        markers.sort((a, b) => a.start - b.start);

        // Create segments
        markers.forEach((marker) => {
            // Add text before the marker
            if (currentIndex < marker.start) {
                segments.push({
                    type: 'normal',
                    content: abstractText.substring(currentIndex, marker.start),
                    key: segmentIndex++
                });
            }

            // Add the highlighted segment
            segments.push({
                type: marker.type,
                content: marker.content,
                key: segmentIndex++
            });

            currentIndex = marker.end;
        });

        // Add remaining text after the last marker
        if (currentIndex < abstractText.length) {
            segments.push({
                type: 'normal',
                content: abstractText.substring(currentIndex),
                key: segmentIndex++
            });
        }

        return segments.map(segment => {
            if (segment.type === 'objective') {
                return (
                    <span key={segment.key} className="abstract-objective">
                        {segment.content}
                    </span>
                );
            } else if (segment.type === 'conclusion') {
                return (
                    <span key={segment.key} className="abstract-conclusion">
                        {segment.content}
                    </span>
                );
            } else {
                return segment.content;
            }
        });
    };

    const handleBackToObjetivo = () => {
        setCurrentStep('objetivo');
        setSelectedSentences([]);
        setSelectedNone(false);
        setMatchResult(null);
    };

    const resetAnalysis = () => {
        setCurrentStep('objetivo');
        setObjetivoData(null);
        setConclusaoData(null);
        setSelectedSentences([]);
        setSelectedNone(false);
        setMatchResult(null);
    };

    const renderAnalysisStep = (stepData, stepType, stepTitle) => {
        if (loading) {
            return <Typography>Carregando...</Typography>;
        }

        // Show loading state if we haven't attempted to load yet
        if (!stepData && !hasAttemptedLoad) {
            return <Typography>Carregando...</Typography>;
        }

        // Only show error if we've attempted to load but failed
        if (!stepData && hasAttemptedLoad && !loading) {
            return <Typography>Erro ao carregar o resumo.</Typography>;
        }

        return (
            <>
                <Typography level="body-md bold" className="modal-title">
                    Qual(is) das sentenças do resumo abaixo caracteriza(m) {stepType}?
                </Typography>

                <Box className="sentence-container">
                    {stepData.sentences.map((sentence, index) => {
                        let className = 'sentence-option';
                        
                        // Apply classes based on match result
                        if (matchResult) {
                            // Use required_sentences if available (complete verification), otherwise fall back to flexible matching
                            const correctIndices = matchResult.required_sentences || 
                                (matchResult.annotated_phrase ? stepData.sentences
                                    .map((s, idx) => {
                                        const annotatedPhrase = matchResult.annotated_phrase;
                                        return (annotatedPhrase.includes(s) || s.includes(annotatedPhrase)) ? idx : -1;
                                    })
                                    .filter(idx => idx !== -1) : []);
                            
                            if (selectedSentences.includes(index)) {
                                // User's selected answer
                                if (correctIndices.includes(index)) {
                                    // Selected sentence is part of correct answer
                                    className += ' correct';
                                } else {
                                    // Selected sentence is incorrect (extra selection)
                                    className += ' incorrect';
                                }
                            } else if (correctIndices.includes(index) && !matchResult.match) {
                                // Show missing correct answer when user is wrong
                                className += ' correct';
                            }
                        } else if (selectedSentences.includes(index)) {
                            // Normal selected state when no result yet
                            className += ' selected';
                        }
                        
                        return (
                            <Box 
                                key={index}
                                className={className}
                                onClick={() => handleSentenceSelect(index)}
                            >
                                <Typography level="body-sm">
                                    <strong>{index + 1}:</strong> {sentence}
                                </Typography>
                            </Box>
                        );
                    })}
                    
                    {/* Nenhuma das opções button */}
                    <Box 
                        className={`none-option ${(() => {
                            if (matchResult) {
                                return selectedNone ? (matchResult.match ? 'correct' : 'incorrect') : '';
                            }
                            return selectedNone ? 'selected' : '';
                        })()}`}
                        onClick={handleNoneSelect}
                    >
                        <Typography level="body-sm" className={`none-option-text ${(() => {
                            if (matchResult) {
                                return selectedNone ? (matchResult.match ? 'correct' : 'incorrect') : '';
                            }
                            return selectedNone ? 'selected' : '';
                        })()}`}>
                            Nenhuma das opções
                        </Typography>
                        <Typography level="body-xs" className={`none-option-subtext ${(() => {
                            if (matchResult) {
                                return selectedNone ? (matchResult.match ? 'correct' : 'incorrect') : '';
                            }
                            return selectedNone ? 'selected' : '';
                        })()}`}>
                            Selecione se não há {stepType} claro no resumo
                        </Typography>
                    </Box>
                </Box>

                {(selectedSentences.length > 0 || selectedNone) && !matchResult && (
                    <Box className="button-container-centered-verify">
                        <Button 
                            variant="solid" 
                            color="success"
                            onClick={handleCheckMatch}
                            disabled={loading}
                            className="modal-action-button modal-verify-button"
                        >
                            Verificar Resposta
                        </Button>
                    </Box>
                )}

                {matchResult && (
                    <>
                        <div className="modal-divider"></div>
                        <Box className={`result-box ${matchResult.match ? 'success' : 'error'}`}>
                        <Typography level="body-sm" className="modal-result-text">
                            <strong>Resultado:</strong> {matchResult.match ? 'Correto!' : 'Incorreto'}
                        </Typography>
                        
                        {/* <Typography level="body-xs" className="modal-result-detail">
                            <strong>Sua escolha:</strong> {matchResult.user_phrase}
                        </Typography>
                        <Typography level="body-xs" className="modal-result-detail">
                            <strong>Frase anotada:</strong> {matchResult.annotated_phrase}
                        </Typography> */}

                        <Chip 
                            className="modal-result-chip"
                            size="sm"
                        >
                            {stepData.categoria}: {stepData.justificativa}
                        </Chip>
                        </Box>
                    </>
                )}

                <Box className="button-container-centered">
                    
                    {matchResult && (
                        <Button 
                            variant="solid" 
                            color="primary"
                            onClick={handleNextStep}
                            className="modal-action-button modal-next-button"
                        >
                            {currentStep === 'objetivo' ? 'Próximo: Análise de Conclusão' : 'Finalizar Análise'}
                        </Button>
                    )}
                </Box>
            </>
        );
    };

    return (
        <Modal open={open} onClose={() => {}}>
            <ModalDialog 
              size="lg"
              color="neutral"
              variant="soft"
              className="modal-dialog"
            >
                <ModalClose onClick={() => onClose(false)} />
                
                {currentStep === 'complete' ? (
                    // Completion screen
                    <>
                        <DialogTitle className="modal-dialog-title">Parabéns! Análise Concluída!</DialogTitle>
                        <DialogContent>
                            <Typography level="body-md" className="modal-completion-title">
                                <strong>Resumo {resumo?.id}:</strong> {resumo?.titulo}
                            </Typography>
                            <Box className="abstract-overview">
                                <Typography level="body-sm" className="abstract-overview-text">
                                    {renderHighlightedAbstract(resumo?.resumo)}
                                </Typography>
                            </Box>
                            
                            {/* Legend for highlighting colors */}
                            <Box className="abstract-legend">
                                <Box className="legend-item">
                                    <Box className="legend-color legend-objective"></Box>
                                    <Typography level="body-xs">Objetivo</Typography>
                                </Box>
                                <Box className="legend-item">
                                    <Box className="legend-color legend-conclusion"></Box>
                                    <Typography level="body-xs">Conclusão</Typography>
                                </Box>
                            </Box>
                            
                            <Box className="button-container-centered">
                                <Button 
                                    variant="outlined" 
                                    color="neutral"
                                    onClick={() => onClose(false)}
                                    className="modal-action-button modal-close-button"
                                >
                                    Fechar
                                </Button>
                            </Box>
                        </DialogContent>
                    </>
                ) : (
                    // Analysis screen (objetivo or conclusao)
                    <>
                        <DialogTitle className="modal-dialog-title">
                            <Typography level="body-lg" className="modal-title">
                                Artigo: {resumo?.titulo}
                            </Typography>
                        </DialogTitle>
                        <DialogContent>
                            {currentStep === 'objetivo' 
                                ? renderAnalysisStep(objetivoData, 'objetivo', 'Objetivo')
                                : renderAnalysisStep(conclusaoData, 'conclusão', 'Conclusão')
                            }
                        </DialogContent>
                    </>
                )}
            </ModalDialog>
        </Modal>
    );
};

export default CaixaDialogo;