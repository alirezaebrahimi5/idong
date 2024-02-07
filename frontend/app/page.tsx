"use client"

import { BrowserRouter, Route, Routes } from 'react-router-dom';

import Home from "@/app/pages/Home";
import Login from "@/app/pages/Login";

import './App.css';

import { useEffect, useState } from 'react';


function App() {

  const [loggedIn, setLoggedIn] = useState(false)

  const [email, setEmail] = useState("")


  return (

    <div className="App">

      <BrowserRouter>

        <Routes>

          <Route path="/" element={<Home email={email} loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>} />

          <Route path="/login" element={<Login setLoggedIn={setLoggedIn} setEmail={setEmail} />} />

        </Routes>

      </BrowserRouter>

    </div>

  );

}


export default App;