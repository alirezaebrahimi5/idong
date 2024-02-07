import React, { useState } from "react";

import { useNavigate } from "react-router-dom";
import axios from "axios";


const Login = (props: any) => {

    const [email, setEmail] = useState("")

    const [emailError, setEmailError] = useState("")


    const navigate = useNavigate();


  const fetchLogin = async(e: any) => {
    e.preventDefault()
    const api = "http://localhost:8000/auth/email/"
    const formData = new FormData();
    formData.append("email", email);
    await axios.post(api, formData,{
            headers: {
                "content-type": "multipart/form-data",
            },
    }).then((response) => {
        if(response.status===201) {
          navigate("/check");
        }

      });
    }



const onButtonClick = (e: any) => {


        // Set initial error values to empty

        setEmailError("")

        // Check if the user has entered both fields correctly

        if ("" === email) {

            setEmailError("Please enter your email")

            return

        } else {
            fetchLogin(e)
        }


        if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {

            setEmailError("Please enter a valid email")

            return

        }


    }


    return <div className={"mainContainer"}>

        <div className={"titleContainer"}>

            <div>Login</div>

        </div>

        <br />

        <div className={"inputContainer"}>

            <input

                value={email}

                placeholder="Enter your email here"

                onChange={ev => setEmail(ev.target.value)}

                className={"inputBox"} />

            <label className="errorLabel">{emailError}</label>

        </div>

        <br />

        <div className={"inputContainer"}>

            <input

                className={"inputButton"}

                type="button"

                onClick={onButtonClick}

                value={"Log in"} />

        </div>

    </div>

}


export default Login