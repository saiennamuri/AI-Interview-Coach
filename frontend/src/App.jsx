import { useState } from "react";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";


function App() {

    const [user, setUser] = useState(null);

    const [showRegister, setShowRegister] =
        useState(false);


    const handleLogout = () => {

        setUser(null);

        setShowRegister(false);

    };


    /* =============================== */
    /* Logged In */
    /* =============================== */

    if (user) {

        return (

            <Dashboard
                user={user}
                onLogout={handleLogout}
            />

        );

    }


    /* =============================== */
    /* Register */
    /* =============================== */

    if (showRegister) {

        return (

            <div>

                <Register />


                <div
                    style={{
                        textAlign: "center",
                        marginTop: "15px"
                    }}
                >

                    <p>
                        Already have an account?
                    </p>


                    <button
                        onClick={() =>
                            setShowRegister(false)
                        }
                    >
                        Login
                    </button>

                </div>

            </div>

        );

    }


    /* =============================== */
    /* Login */
    /* =============================== */

    return (

        <div>

            <Login
                onLogin={setUser}
            />


            <div
                style={{
                    textAlign: "center",
                    marginTop: "15px"
                }}
            >

                <p>
                    Don't have an account?
                </p>


                <button
                    onClick={() =>
                        setShowRegister(true)
                    }
                >
                    Register
                </button>

            </div>

        </div>

    );

}


export default App;