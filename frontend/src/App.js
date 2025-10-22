import './style/App.css';
import Header from './util/header.js';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Header />
      </header>
      <div className="App-title">
        <h1>BouvetRadar</h1>
      </div>
      <main className='App-main'>
        <p>
          Velkommen til BouvetRadar!
        </p>
      </main>
    </div>
  );
}

export default App;
