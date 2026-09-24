import { useState } from "react";

import ResumeUpload from "./ResumeUpload";
import InterviewSetup from "./InterviewSetup";
import QuestionInterface from "./QuestionInterface";
import InterviewResult from "./InterviewResult";
import InterviewHistory from "./InterviewHistory";


function Dashboard({ user, onLogout }) {

    const [currentPage, setCurrentPage] =
        useState("dashboard");

    const [interview, setInterview] =
        useState(null);


    const goToDashboard = () => {

        setCurrentPage("dashboard");

    };


    const handleInterviewCreated = (newInterview) => {

        setInterview(newInterview);

        setCurrentPage("interview");

    };


    const handleLogout = () => {

        if (onLogout) {

            onLogout();

        }

    };


    /* ================================= */
    /* Dashboard Home */
    /* ================================= */

    if (currentPage === "dashboard") {

        return (

            <div className="dashboard-page">


                {/* =============================== */}
                {/* Top Header */}
                {/* =============================== */}

                <header className="dashboard-top">


                    <div className="dashboard-brand">

                        <div className="brand-icon">
                            🤖
                        </div>


                        <div>

                            <h1>
                                AI Interview Coach
                            </h1>

                            <p>
                                Your AI-powered interview
                                preparation assistant
                            </p>

                        </div>

                    </div>


                    {/* User Area */}

                    {user && (

                        <div className="dashboard-user-area">


                            <div className="dashboard-user">

                                <span className="user-avatar">

                                    {user.name
                                        ?.charAt(0)
                                        .toUpperCase()
                                    }

                                </span>


                                <div className="user-info">

                                    <strong>
                                        {user.name}
                                    </strong>

                                    <small>
                                        Candidate
                                    </small>

                                </div>

                            </div>


                            <button
                                className="logout-button"
                                onClick={handleLogout}
                            >
                                🚪 Logout
                            </button>

                        </div>

                    )}

                </header>


                {/* =============================== */}
                {/* Welcome */}
                {/* =============================== */}

                <main className="dashboard-home">


                    <div className="dashboard-welcome">

                        <p className="welcome-label">
                            INTERVIEW PREPARATION
                        </p>

                        <h2>
                            Welcome, {user?.name}! 👋
                        </h2>

                        <p>
                            Choose an option below to
                            continue your interview
                            preparation.
                        </p>

                    </div>


                    {/* =============================== */}
                    {/* Dashboard Options */}
                    {/* =============================== */}

                    <div className="dashboard-options">


                        {/* Resume */}

                        <div
                            className="dashboard-option resume-option"
                            onClick={() =>
                                setCurrentPage("resume")
                            }
                        >

                            <div className="option-icon">
                                📄
                            </div>


                            <h3>
                                Resume Upload
                            </h3>


                            <p>
                                Upload your resume and
                                extract your technical
                                skills using NLP.
                            </p>


                            <button>
                                Upload Resume →
                            </button>

                        </div>


                        {/* Interview */}

                        <div
                            className="dashboard-option interview-option"
                            onClick={() =>
                                setCurrentPage(
                                    "create-interview"
                                )
                            }
                        >

                            <div className="option-icon">
                                🎯
                            </div>


                            <h3>
                                Create Interview
                            </h3>


                            <p>
                                Create a personalized
                                interview based on
                                your job role.
                            </p>


                            <button>
                                Start Interview →
                            </button>

                        </div>


                        {/* History */}

                        <div
                            className="dashboard-option history-option"
                            onClick={() =>
                                setCurrentPage("history")
                            }
                        >

                            <div className="option-icon">
                                📊
                            </div>


                            <h3>
                                Previous Interviews
                            </h3>


                            <p>
                                View your previous
                                interviews and track
                                your performance.
                            </p>


                            <button>
                                View History →
                            </button>

                        </div>

                    </div>


                    {/* =============================== */}
                    {/* Footer */}
                    {/* =============================== */}

                    <div className="dashboard-footer">

                        <span>
                            🤖 AI Interview Coach
                        </span>

                        <span>
                            Practice • Improve • Succeed
                        </span>

                    </div>

                </main>

            </div>

        );

    }


    /* ================================= */
    /* Resume Page */
    /* ================================= */

    if (currentPage === "resume") {

        return (

            <div className="inner-page">

                <button
                    className="back-button"
                    onClick={goToDashboard}
                >
                    ← Back to Dashboard
                </button>


                <div className="inner-page-header">

                    <h1>
                        📄 Resume Upload
                    </h1>

                    <p>
                        Upload your resume and extract
                        your technical skills.
                    </p>

                </div>


                <div className="inner-page-card">

                    <ResumeUpload
                        user={user}
                    />

                </div>

            </div>

        );

    }


    /* ================================= */
    /* Create Interview */
    /* ================================= */

    if (currentPage === "create-interview") {

        return (

            <div className="inner-page">

                <button
                    className="back-button"
                    onClick={goToDashboard}
                >
                    ← Back to Dashboard
                </button>


                <div className="inner-page-header">

                    <h1>
                        🎯 Create Interview
                    </h1>

                    <p>
                        Choose your job role and
                        interview preferences.
                    </p>

                </div>


                <div className="inner-page-card">

                    <InterviewSetup
                        user={user}
                        onInterviewCreated={
                            handleInterviewCreated
                        }
                    />

                </div>

            </div>

        );

    }


    /* ================================= */
    /* History */
    /* ================================= */

    if (currentPage === "history") {

        return (

            <div className="inner-page">

                <button
                    className="back-button"
                    onClick={goToDashboard}
                >
                    ← Back to Dashboard
                </button>


                <div className="inner-page-header">

                    <h1>
                        📊 Previous Interviews
                    </h1>

                    <p>
                        Review your previous interview
                        performance.
                    </p>

                </div>


                <div className="inner-page-card">

                    <InterviewHistory
                        user={user}
                    />

                </div>

            </div>

        );

    }


    /* ================================= */
    /* Interview */
    /* ================================= */

    if (currentPage === "interview") {

        return (

            <div className="inner-page">

                <button
                    className="back-button"
                    onClick={goToDashboard}
                >
                    ← Back to Dashboard
                </button>


                <div className="inner-page-header">

                    <h1>
                        🎤 Interview
                    </h1>

                    <p>
                        Answer the questions and
                        receive AI-powered feedback.
                    </p>

                </div>


                <div className="inner-page-card">

                    <QuestionInterface
                        interview={interview}
                    />

                </div>


                <div className="inner-page-card">

                    <InterviewResult
                        interview={interview}
                    />

                </div>

            </div>

        );

    }

}


export default Dashboard;