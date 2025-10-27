import './style/App.css';
import './style/MainPage.css';
import Header from './components/header.js';
import Footer from './components/footer.js';
import MainPage from './components/mainPage.js';

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
        <MainPage />
      </main>
      <footer className="App-footer">
        <Footer />
      </footer>
    </div>
  );
}

export default App;
