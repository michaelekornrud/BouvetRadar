import './style/App.css';
import Header from './util/header.js';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Header />
      </header>
      <main className='App-main'>
        <p>
          Velkommen til BouvetRadar!
        </p>
        <p1>
          This is a new paragraph added to enhance the content.
        </p1>
      </main>
    </div>
  );
}

export default App;
