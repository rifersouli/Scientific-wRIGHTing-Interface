import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './BotoesResumos.css';
import CaixaDialogo from './CaixaDialogo';

const BotoesResumos = () => {

  const [resumos, setResumos] = useState([]);
  const [modalAberto, abrirModal] = useState(false);
  const [resumoSelecionado, setResumoSelecionado] = useState(null);

  const handleModalAberto = (resumo) => {
    setResumoSelecionado(resumo);
    abrirModal(true);
  };

  const handleModalFechado = () => {
    abrirModal(false);
  };

  useEffect(() => {
    // Coleta os resumos do backend
    axios.get('http://127.0.0.1:5000/api/Resumos')
      .then(response => {
        setResumos(response.data.resumos || []);
        console.log(response.data);
      })
      .catch(error => console.error('Erro ao coletar os resumos:', error));
  }, []);

  const handleButtonClick = (resumoId) => {
    console.log(`Botão clicado para o id do resumo: ${resumoId}`);
    const resumo = resumos.find((r) => r.id === resumoId);
    if (resumo) {
      handleModalAberto(resumo);
    }
  };

  return (
    <div className="Botoes-grid">
      {resumos && resumos.map(Resumo => (
        <div className="Botoes-grid-item" key={Resumo.id}>
          <button 
          className="Botoes" 
          key={Resumo.id} 
          onClick={() => handleButtonClick(Resumo.id)}
          >
            <h1>{Resumo.id}</h1>
          </button>
        </div>
      ))}

      {/* Render the modal component */}
      {resumoSelecionado && (
        <CaixaDialogo
          open={modalAberto}
          onClose={handleModalFechado}
          resumo={resumoSelecionado}
        />
      )}

    </div>
  );
};

export default BotoesResumos;