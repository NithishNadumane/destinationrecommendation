import React,{useState} from 'react'
import '../css/navbar.css'
import Belike from '../component/belike.png';
// import Auth from '../component/auth.jsx';
const navbar = () => {
  const [showauth, setshowauth] = useState(false);
  const [login,setlogin] = useState(true)
  return (
    <>
      <nav className='navbar'>
        <div className='logo'>
          <img src={Belike} alt="logo" />
          <h1 className='logoname'>BeLikeTraveller</h1>
        </div>
        <div >
          <ul className='li'>
            <li>Home</li>
            <li>About</li>
            <li>Services</li>
          </ul>
        </div>
        <div>
          <button onClick={()=>{setshowauth(!showauth)}}>Signin/Signup</button>
        </div>
      </nav>
    
    </>
  )
}

export default navbar
