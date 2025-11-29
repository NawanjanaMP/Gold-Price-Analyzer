import React from 'react'
import ReactDOM from 'react-dom/client'
import GoldPriceAnalyzer from './GoldPriceAnalyzer'
import ErrorBoundary from './ErrorBoundary'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ErrorBoundary>
      <GoldPriceAnalyzer />
    </ErrorBoundary>
  </React.StrictMode>,
)
