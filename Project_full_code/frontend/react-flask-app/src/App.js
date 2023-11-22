import logo from './LogotipoScientificWrighting.png';
import './App.css';
import BotoesResumos from './components/BotoesResumos';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
      </header>
      <div className="App-body">

        <div className="App-text">
          <p><mark>ㅤEscolha um resumo para treinar sua escrita científica:ㅤㅤㅤㅤㅤㅤ</mark></p>
        </div>
        
        <BotoesResumos />
      </div>

    </div>
  );
}

export default App;
