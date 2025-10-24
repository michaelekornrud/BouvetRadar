import './style/App.css';
import './style/MainPage.css';
import Header from './util/header.js';
import Footer from './util/footer.js';
import MainPage from './util/mainPage.js';
import CPVCategoriesList from './importData.js';

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
        <CPVCategoriesList />
      </main>
      <footer className="App-footer">
        <Footer />
      </footer>
    </div>
  );
}

export default App;
