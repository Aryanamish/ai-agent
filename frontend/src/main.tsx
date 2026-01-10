import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { ShopwiseRoutes } from './routes'
import { BrowserRouter } from 'react-router'








createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
    <ShopwiseRoutes />
    </BrowserRouter>
  </StrictMode>,
)
