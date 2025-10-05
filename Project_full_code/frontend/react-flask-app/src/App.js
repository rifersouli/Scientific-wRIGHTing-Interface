import logo from './LogotipoScientificWrighting.png';
import './App.css';
import BotoesResumos from './components/BotoesResumos';

function App() {

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <title>Scientific wRIGHTing</title>
      </header>
      <div className="App-body">

        <div className="App-text">
          <div className="App-text-container">
            Escolha um resumo para treinar sua escrita científica:
          </div>
        </div>

        <BotoesResumos />
      </div>

    </div>
  );
}

export default App;
