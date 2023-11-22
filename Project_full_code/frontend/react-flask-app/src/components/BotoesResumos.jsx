import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './BotoesResumos.css';

const BotoesResumos = () => {
  const [resumos, setResumos] = useState([]);

  useEffect(() => {
    // Fetch resumos data from the Flask backend
    axios.get('http://127.0.0.1:5000/api/Resumos')
      .then(response => {
        setResumos(response.data.resumos || []);
        console.log(response.data);
      })
      .catch(error => console.error('Error fetching abstracts:', error));
  }, []);

  return (
    <div className="Botoes-grid">
      {resumos && resumos.map(Resumo => (
        <div className="Botoes-grid-item" key={Resumo.id}>
          <button className="Botoes" key={Resumo.id} onClick={() => handleButtonClick(Resumo.id)}>
            <h1>{Resumo.id}</h1>
          </button>
        </div>
      ))}
    </div>
  );
};

const handleButtonClick = (resumoId) => {
  // Handle button click logic
  console.log(`Botão clicado para o id do resumo: ${resumoId}`);
};

export default BotoesResumos;