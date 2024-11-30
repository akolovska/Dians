import "./navBar.css"
import {Link} from "react-router-dom";

function navBar() {
    return (
    <ul>
        <li><Link to="/FundamentalAnalysis.tsx">logo</Link></li>
        <li>Technical analysis</li>
        <li>Fundamental analysis</li>
        <li>LSTM</li>
        <li>Individual company analysis</li>
        <li>Download data</li>
        <li>About us</li>
    </ul>
    )
}

export default navBar()