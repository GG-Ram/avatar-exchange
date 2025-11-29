import { Routes, Route, Navigate } from "react-router-dom";
import MarketPage from "./pages/marketPage/MarketPage.jsx";
import Navbar from "./components/NavBar/Navbar";
import ShopPage from "./pages/ShopPage/ShopPage";
import { UserProvider } from "./Hooks/userContext.jsx";
import Portfolio from "./pages/Portfolio/Portfolio.jsx";
import AvatarPage from './pages/AvatarPage/AvatarPage.jsx';
import Transactions from './pages/Transactions/Transactions.jsx';
import Analytics from './pages/Analytics/Analytics.jsx';
import Leaderboard from './pages/Leaderboard/Leaderboard.jsx';
import Login from "./components/Auth/Login.jsx";
import Register from "./components/Auth/Register.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import "./app.css";



function App() {
  return (
    <div style={{ padding: 20 }}>
      {/* Routes */}
      <UserProvider>
      <Navbar/>
      
      <Routes>
        <Route path="/" element={<Navigate to="/market" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route 
          path="/market" 
          element={
            <ProtectedRoute>
              <MarketPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/shop" 
          element={
            <ProtectedRoute>
              <ShopPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/avatar" 
          element={
            <ProtectedRoute>
              <AvatarPage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/Portfolio" 
          element={
            <ProtectedRoute>
              <Portfolio />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/transactions" 
          element={
            <ProtectedRoute>
              <Transactions />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/analytics" 
          element={
            <ProtectedRoute>
              <Analytics />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/leaderboard" 
          element={
            <ProtectedRoute>
              <Leaderboard />
            </ProtectedRoute>
          } 
        />
      </Routes>
     </UserProvider>
    </div>
  );
}

export default App;
