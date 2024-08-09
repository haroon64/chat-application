import React, { useState, useEffect } from 'react';
// import 'bootstrap/dist/css/bootstrap.min.css';
import { useNavigate } from 'react-router-dom';
import Axios from 'axios';
import {AiOutlineLogin,AiOutlineUserAdd} from 'react-icons/ai'
import Cookies from 'js-cookie';
import "./styles/login.css"

function LoginForm() 
{
// const token = Cookies.get('token');

const navigate = useNavigate()
// const onLoginPress = () => {
//   navigate('/Home')
// }

const [error, setError] = useState("");
const [username, setUsername] = useState('');
const [password, setPassword] = useState('');



const handleChangeusername = event => {
setUsername(event.target.value);
}
const handleChangepassword = event => {
setPassword(event.target.value);
}
const GoToSignup = e => {
  e.preventDefault();
  navigate('/Signup');
  };
const errorfield = document.getElementById("errorfield");

const handleLogin = async (e) => {
  e.preventDefault();
  try {
      const response = await Axios.post('http://localhost:8000/api/v1/auth/sign-in', {
          email: username,
          password: password
      });
      const client_id=response.data.user_info.id

      Cookies.set('token', response.data.access_token, { expires: 6, sameSite: 'strict' });
      Axios.defaults.headers.common['Authorization'] = `Bearer ${Cookies.get('token')}`;
      navigate('/ChatRoom', { state: { client_id } });
  } catch (err) {
      if (err.response && err.response.status === 401) {
          setError('Invalid email or password');
      } else {
          setError('An error occurred. Please try again.');
      }
  }
};
return (
    <div>
        <div className="sub-container ">
            <h1 style={{color:"white"}}>Login <span className="badge bg-new-2">Portal</span></h1>
            <div>
                <form id = "signup-form">
                    
                    <input onChange={handleChangeusername} value={username} type="text"className="form-control margin-top"id="id"placeholder="enter Email"/>
                    <input onChange={handleChangepassword}type="password" value={password}className="form-control margin-top"id="password"placeholder="Enter password"/>
                    <div><h6 id="errorfield" style={{ color: 'red' }}>{error}</h6></div>

                    <a href="#" className="text-decoration-none margin-top"style={{color:"white"}}>Forget Password?</a>
                  </form>
                <form style={{display:'flex',flexDirection:'column'}}>
                  <div className="btn-group-vertical">
                      <button onClick={(e) => { handleLogin(e)}}  type="submit" className="btn btn-info margin-top "> Login<AiOutlineLogin/></button>
                      <button onClick={(e) => { GoToSignup(e)}}  type="submit" className="btn btn-primary margin-top "> Signup<AiOutlineUserAdd/></button>
            
                    </div>
                  </form>
          </div>
      </div>
    </div>
);
}


export default LoginForm;