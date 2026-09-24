import { useState } from "react";
import api from "../services/api";


function Login({ onLogin }) {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [message, setMessage] = useState("");
    const [error, setError] = useState("");


    const handleLogin = async (e) => {

        e.preventDefault();

        setMessage("");
        setError("");


        try {

            const response = await api.post(
                "/users/login",
                {
                    email: email,
                    password: password
                }
            );


            setMessage(response.data.message);


            if (onLogin) {

                onLogin(response.data.data);

            }


        } catch (err) {

            if (err.response) {

                setError(
                    err.response.data.message ||
                    "Login failed"
                );

            } else {

                setError(
                    "Unable to connect to the server"
                );

            }

        }

    };


    return (

        <div className="auth-container">

            <div className="auth-card">

                <h1>AI Interview Coach</h1>

                <p className="auth-subtitle">
                    Practice. Improve. Succeed.
                </p>


                <h2>Login</h2>


                <form onSubmit={handleLogin}>

                    <label>
                        Email
                    </label>

                    <input
                        type="email"
                        placeholder="Enter your email"
                        value={email}
                        onChange={(e) =>
                            setEmail(e.target.value)
                        }
                        required
                    />


                    <label>
                        Password
                    </label>

                    <input
                        type="password"
                        placeholder="Enter your password"
                        value={password}
                        onChange={(e) =>
                            setPassword(e.target.value)
                        }
                        required
                    />


                    <button
                        type="submit"
                        className="primary-btn"
                    >
                        Login
                    </button>

                </form>


                {message && (

                    <p className="success-message">
                        {message}
                    </p>

                )}


                {error && (

                    <p className="error-message">
                        {error}
                    </p>

                )}

            </div>

        </div>

    );
}


export default Login;