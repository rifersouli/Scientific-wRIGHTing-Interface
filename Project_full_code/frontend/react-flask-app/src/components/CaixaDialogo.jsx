import React from 'react'
import Button from '@mui/joy/Button';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Input from '@mui/joy/Input';
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';
import DialogTitle from '@mui/joy/DialogTitle';
import DialogContent from '@mui/joy/DialogContent';
import Stack from '@mui/joy/Stack';

const CaixaDialogo = ({ open = false, onClose, resumo }) => {
    return (

        <Modal open={open} onClose={() => onClose(false)}>
            <ModalDialog 
              size="lg"
              color="neutral"
              variant="soft"
            >
                <ModalClose></ModalClose>
                <DialogTitle>Qual(is) das sentenças do resumo caracteriza(m) Objetivo?</DialogTitle>
                <DialogContent>{resumo.resumo}
                    <p>Em indústrias de manufatura, um dos processos de produção consiste em cortar grandes objetos em peças menores.</p>
                    <p>Em pesquisa operacional, o estudo desse processo é conhecido como o problema de corte de estoque (PCE) e, devido a sua dificuldade de resolução, métodos heurísticos vem sendo desenvolvidos pelos pesquisadores da área.</p>
                    <p>Neste trabalho, propomos utilizar técnicas de análise de decisão multicritério (MCDA) a fim de resolver o PCE de forma eficiente em termos de GAP e tempo computacional.</p>
                    <p>Nossa estratégia consiste em selecionar previamente os melhores padrões de corte com técnicas MCDA e resolver o problema apenas com esses padrões selecionados.</p>
                    <p>Os testes computacionais mostraram que a solução obtida com essa estratégia apresenta um GAP entre 0,25% e 4,25% quando comparada com a solução ótima, dando indícios da qualidade da abordagem proposta.</p>
                </DialogContent>
                <button className='BotaoNenhumaAlternativa'>
                    <h3>Nenhuma das alternativas</h3>
                </button>
                {console.log(resumo.resumo)}
            </ModalDialog>
        </Modal>

    );
};

export default CaixaDialogo;