import React from "react"

import { useNavigate } from "react-router-dom";


const Check = (props: any) => {

    const { loggedIn, email } = props

    const navigate = useNavigate();


    return <div className="mainContainer">

        <div className={"titleContainer"}>

            <div>ok!</div>

        </div>

        <div>

            Check your email.

        </div>




    </div>

}


export default Check