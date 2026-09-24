import { useState } from "react";
import api from "../services/api";


function Register() {

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const [message, setMessage] = useState("");
    const [error, setError] = useState("");


    const handleRegister = async (e) => {

        e.preventDefault();

        setMessage("");
        setError("");


        try {

            const response = await api.post(
                "/users/register",
                {
                    name: name,
                    email: email,
                    password: password
                }
            );


            setMessage(response.data.message);


            setName("");
            setEmail("");
            setPassword("");


        } catch (err) {

            if (err.response) {

                setError(
                    err.response.data.message ||
                    "Registration failed"
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
                    Create your account
                </p>


                <h2>Register</h2>


                <form onSubmit={handleRegister}>

                    <label>
                        Full Name
                    </label>

                    <input
                        type="text"
                        placeholder="Enter your full name"
                        value={name}
                        onChange={(e) =>
                            setName(e.target.value)
                        }
                        required
                    />


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
                        placeholder="Create a password"
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
                        Create Account
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


export default Register;