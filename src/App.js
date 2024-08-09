import './App.css';
import Login from './LoginForm';
import Signup from './SignupForm';
import ChatRoom from './ChatRoom';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path='/login' element={<Login />} />
          <Route path='/signup' element={<Signup />} />
          <Route path='/chatroom' element={<ChatRoom />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
