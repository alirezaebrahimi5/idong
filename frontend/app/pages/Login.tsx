import React, { useState } from "react";

import { useNavigate } from "react-router-dom";


const Login = (props: any) => {

    const [email, setEmail] = useState("")

    const [password, setPassword] = useState("")

    const [emailError, setEmailError] = useState("")

    const [passwordError, setPasswordError] = useState("")



    const navigate = useNavigate();



const onButtonClick = () => {


        // Set initial error values to empty

        setEmailError("")

        setPasswordError("")


        // Check if the user has entered both fields correctly

        if ("" === email) {

            setEmailError("Please enter your email")

            return

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