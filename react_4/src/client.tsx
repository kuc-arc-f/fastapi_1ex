import ReactDOM from 'react-dom/client'
import React from 'react'
import { BrowserRouter } from "react-router";

function App() {
return (
  <div>
    <h1 class="text-3xl">hello</h1>
  </div>
);
}

ReactDOM.createRoot(document.getElementById('app')).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
)
console.log('createRoot')
