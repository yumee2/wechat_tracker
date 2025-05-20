import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/layout/Header';
import CalculatorPage from './pages/CalculatorPage/CalculatorPage';
import CurrencyPage from './pages/CurrencyPage/CurrencyPage';
import baseIcon from '../public/baseIcon.png'
import CasesPage from './pages/CasesPage/CasesPage';
import ProductPage from './pages/CasesPage/ProductCardComponents/ProductPage'

function App() {
  return (
    // <Router>
    //   <div className="App">
    //     <Header />
    //     <Routes>
    //       <Route path="/" element={<CalculatorPage />} />
    //       <Route path="/currency" element={<CurrencyPage />} />
    //       <Route path="/cases" element={<CasesPage />} />
    //     </Routes>
    //     <button className="baseIcon">
    //       <img src={baseIcon} alt="baseIcon" />
    //     </button>
    //   </div>
    // </Router>
    <Router>
      <div className="App">
        <Routes>
          <Route path="/product/:productId" element={<ProductPage />} />
          <Route path="*" element={
            <>
              <Header />
              <Routes>
                <Route path="/" element={<CalculatorPage />} />
                <Route path="/currency" element={<CurrencyPage />} />
                <Route path="/cases" element={<CasesPage />} />
              </Routes>
              <button className="baseIcon">
                <img src={baseIcon} alt="baseIcon" />
              </button>
            </>
          } />
        </Routes>
      </div>
    </Router>
  )
}

export default App
