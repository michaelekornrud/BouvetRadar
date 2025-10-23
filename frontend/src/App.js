import './style/App.css';
import './style/MainPage.css';
import Header from './util/header.js';
import Footer from './util/footer.js';
import JobCard from './util/jobCard.js';

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
        <div className='Card'>
          <JobCard
            employer="Bouvet"
            title="Frontend Developer"
            location="Sandvika"
            expirationDate="31-12-2025"
            source="LinkedIn"
          />
        </div>
      </main>
      <footer className="App-footer">
        <Footer />
      </footer>
    </div>
  );
}

export default App;
