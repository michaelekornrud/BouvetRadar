import './style/App.css';
import Header from './util/header.js';
import Footer from './util/footer.js';

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
      <footer className="App-footer">
        <Footer />
      </footer>
    </div>
  );
}

export default App;
