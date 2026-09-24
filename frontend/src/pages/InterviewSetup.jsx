import { useState } from "react";

import api from "../services/api";


function InterviewSetup({ user, onInterviewCreated }) {

    const [jobRole, setJobRole] = useState("");

    const [difficulty, setDifficulty] = useState("Easy");

    const [interviewType, setInterviewType] =
        useState("Technical");

    const [message, setMessage] = useState("");

    const [error, setError] = useState("");

    const [interview, setInterview] = useState(null);


    const handleCreateInterview = async (event) => {

        event.preventDefault();

        setMessage("");
        setError("");
        setInterview(null);


        if (!user) {

            setError(
                "User information is not available"
            );

            return;
        }


        if (!jobRole.trim()) {

            setError(
                "Please enter a job role"
            );

            return;
        }


        try {

            const response = await api.post(
                "/interviews/create",
                {
                    user_id: user.user_id,
                    job_role: jobRole,
                    difficulty: difficulty,
                    interview_type: interviewType
                }
            );


            setMessage(
                response.data.message
            );


            setInterview(
                response.data.data
            );


            onInterviewCreated(
                response.data.data
            );


        } catch (error) {

            console.error(error);


            if (error.response) {

                setError(
                    error.response.data.message
                );

            } else {

                setError(
                    "Could not connect to backend"
                );

            }

        }

    };


    return (

        <div className="interview-setup-content">


            {/* Header */}

            <div className="interview-setup-header">

                <div className="interview-main-icon">
                    🎯
                </div>

                <h2>
                    Create Your Interview
                </h2>

                <p>
                    Customize your interview according
                    to your career goal.
                </p>

            </div>


            {/* Candidate */}

            {user && (

                <div className="candidate-info">

                    <span className="candidate-icon">
                        👤
                    </span>

                    <div>

                        <small>
                            Candidate
                        </small>

                        <strong>
                            {user.name}
                        </strong>

                    </div>

                </div>

            )}


            {/* Form */}

            <form
                className="interview-form"
                onSubmit={handleCreateInterview}
            >


                {/* Job Role */}

                <div className="form-group">

                    <label>
                        💼 Job Role
                    </label>

                    <input
                        type="text"
                        value={jobRole}
                        onChange={(event) =>
                            setJobRole(event.target.value)
                        }
                        placeholder="Example: Python Developer"
                    />

                    <small>
                        Enter the role you are preparing for.
                    </small>

                </div>


                {/* Difficulty */}

                <div className="form-group">

                    <label>
                        📈 Difficulty Level
                    </label>

                    <div className="option-grid">

                        <label
                            className={
                                difficulty === "Easy"
                                    ? "choice-card active-choice"
                                    : "choice-card"
                            }
                        >

                            <input
                                type="radio"
                                name="difficulty"
                                value="Easy"
                                checked={
                                    difficulty === "Easy"
                                }
                                onChange={(event) =>
                                    setDifficulty(
                                        event.target.value
                                    )
                                }
                            />

                            <span>
                                🟢
                            </span>

                            <strong>
                                Easy
                            </strong>

                            <small>
                                Basic concepts
                            </small>

                        </label>


                        <label
                            className={
                                difficulty === "Medium"
                                    ? "choice-card active-choice"
                                    : "choice-card"
                            }
                        >

                            <input
                                type="radio"
                                name="difficulty"
                                value="Medium"
                                checked={
                                    difficulty === "Medium"
                                }
                                onChange={(event) =>
                                    setDifficulty(
                                        event.target.value
                                    )
                                }
                            />

                            <span>
                                🟡
                            </span>

                            <strong>
                                Medium
                            </strong>

                            <small>
                                Practical concepts
                            </small>

                        </label>


                        <label
                            className={
                                difficulty === "Hard"
                                    ? "choice-card active-choice"
                                    : "choice-card"
                            }
                        >

                            <input
                                type="radio"
                                name="difficulty"
                                value="Hard"
                                checked={
                                    difficulty === "Hard"
                                }
                                onChange={(event) =>
                                    setDifficulty(
                                        event.target.value
                                    )
                                }
                            />

                            <span>
                                🔴
                            </span>

                            <strong>
                                Hard
                            </strong>

                            <small>
                                Advanced concepts
                            </small>

                        </label>

                    </div>

                </div>


                {/* Interview Type */}

                <div className="form-group">

                    <label>
                        🧑‍💼 Interview Type
                    </label>

                    <div className="option-grid">

                        <label
                            className={
                                interviewType === "Technical"
                                    ? "choice-card active-choice"
                                    : "choice-card"
                            }
                        >

                            <input
                                type="radio"
                                name="interviewType"
                                value="Technical"
                                checked={
                                    interviewType === "Technical"
                                }
                                onChange={(event) =>
                                    setInterviewType(
                                        event.target.value
                                    )
                                }
                            />

                            <span>
                                💻
                            </span>

                            <strong>
                                Technical
                            </strong>

                            <small>
                                Technical skills
                            </small>

                        </label>


                        <label
                            className={
                                interviewType === "HR"
                                    ? "choice-card active-choice"
                                    : "choice-card"
                            }
                        >

                            <input
                                type="radio"
                                name="interviewType"
                                value="HR"
                                checked={
                                    interviewType === "HR"
                                }
                                onChange={(event) =>
                                    setInterviewType(
                                        event.target.value
                                    )
                                }
                            />

                            <span>
                                🤝
                            </span>

                            <strong>
                                HR
                            </strong>

                            <small>
                                Behavioural skills
                            </small>

                        </label>


                        <label
                            className={
                                interviewType === "Mixed"
                                    ? "choice-card active-choice"
                                    : "choice-card"
                            }
                        >

                            <input
                                type="radio"
                                name="interviewType"
                                value="Mixed"
                                checked={
                                    interviewType === "Mixed"
                                }
                                onChange={(event) =>
                                    setInterviewType(
                                        event.target.value
                                    )
                                }
                            />

                            <span>
                                ⭐
                            </span>

                            <strong>
                                Mixed
                            </strong>

                            <small>
                                Technical + HR
                            </small>

                        </label>

                    </div>

                </div>


                {/* Create button */}

                <button
                    type="submit"
                    className="create-interview-button"
                >
                    🚀 Create Interview
                </button>

            </form>


            {/* Messages */}

            {message && (

                <div className="interview-success">
                    ✓ {message}
                </div>

            )}


            {error && (

                <div className="interview-error">
                    ⚠ {error}
                </div>

            )}


            {/* Created Interview */}

            {interview && (

                <div className="created-interview-card">

                    <div className="created-icon">
                        ✓
                    </div>

                    <div>

                        <h3>
                            Interview Created
                        </h3>

                        <p>
                            Your interview is ready.
                        </p>

                    </div>


                    <div className="interview-details">

                        <div>
                            <small>
                                Interview ID
                            </small>

                            <strong>
                                {interview.interview_id}
                            </strong>
                        </div>


                        <div>
                            <small>
                                Job Role
                            </small>

                            <strong>
                                {interview.job_role}
                            </strong>
                        </div>


                        <div>
                            <small>
                                Difficulty
                            </small>

                            <strong>
                                {interview.difficulty}
                            </strong>
                        </div>


                        <div>
                            <small>
                                Type
                            </small>

                            <strong>
                                {interview.interview_type}
                            </strong>
                        </div>

                    </div>

                </div>

            )}

        </div>

    );

}


export default InterviewSetup;