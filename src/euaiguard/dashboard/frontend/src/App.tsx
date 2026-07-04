import { useState } from 'react'
import Dashboard from './pages/Dashboard'
import './cssFiles/main.css';

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <div>
      <Dashboard />
    </div>
    </>
  )
}

export default App
