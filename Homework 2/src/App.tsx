import "./App.css"
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from "./Home.tsx"
import FundamentalAnalysis from "./FundamentalAnalysis.tsx";
// import IndividualAnalysis from "./IndividualAnalysis.tsx"
// import LSTM from './LSTM.tsx';
// // import CompanyAnalysis from './CompanyAnalysis.tsx';
// import DownloadData from './DownloadData.tsx';
import TechnicalAnalysis from "./TechnicalAnalysis.tsx";
import AboutUs from "./AboutUs.tsx";

function App() {
    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/" element={<Home/>} />
                    <Route path="/FundamentalAnalysis.tsx" element={<FundamentalAnalysis/>} />
                    <Route path="/TechnicalAnalysis.tsx" element={<TechnicalAnalysis/>} />
                    <Route path="/about-us" element={<AboutUs/>} />
                    {/*<Route path="/"*/}
                </Routes>
            </div>
        </Router>
    )
}

export default App