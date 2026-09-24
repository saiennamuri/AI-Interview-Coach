import { useEffect, useState } from "react";

import api from "../services/api";


function InterviewHistory({ user }) {

    const [interviews, setInterviews] =
        useState([]);

    const [selectedResult, setSelectedResult] =
        useState(null);

    const [loading, setLoading] =
        useState(true);

    const [resultLoading, setResultLoading] =
        useState(false);

    const [error, setError] =
        useState("");


    /* ============================= */
    /* Get Interview History */
    /* ============================= */

    const getInterviews = async () => {

        try {

            const response = await api.get(
                `/interviews/user/${user.user_id}`
            );


            setInterviews(
                response.data.data.interviews
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

        } finally {

            setLoading(false);

        }
    };


    /* ============================= */
    /* View Result */
    /* ============================= */

    const viewResult = async (interviewId) => {

        setError("");
        setSelectedResult(null);
        setResultLoading(true);


        try {

            const response = await api.get(
                `/interviews/${interviewId}/result`
            );


            setSelectedResult(
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
                    "Could not retrieve interview result"
                );
            }

        } finally {

            setResultLoading(false);

        }
    };


    /* ============================= */
    /* Load History */
    /* ============================= */

    useEffect(() => {

        if (user) {

            getInterviews();

        }

    }, [user]);


    /* ============================= */
    /* No User */
    /* ============================= */

    if (!user) {

        return (

            <div className="history-empty">

                <div className="history-empty-icon">
                    👤
                </div>

                <h2>
                    User Information Unavailable
                </h2>

                <p>
                    Please login again to view your
                    interview history.
                </p>

            </div>

        );
    }


    return (

        <div className="history-page">


            {/* ================================= */}
            {/* Header */}
            {/* ================================= */}

            <div className="history-header">

                <div className="history-header-icon">
                    📊
                </div>


                <div>

                    <p className="history-header-label">
                        YOUR INTERVIEW JOURNEY
                    </p>

                    <h1>
                        Previous Interviews
                    </h1>

                    <p>
                        Review your practice sessions
                        and track your performance.
                    </p>

                </div>

            </div>


            {/* ================================= */}
            {/* Loading */}
            {/* ================================= */}

            {loading && (

                <div className="history-loading">

                    <div className="history-spinner"></div>

                    <p>
                        Loading your interviews...
                    </p>

                </div>

            )}


            {/* ================================= */}
            {/* Error */}
            {/* ================================= */}

            {error && (

                <div className="history-error">
                    ⚠ {error}
                </div>

            )}


            {/* ================================= */}
            {/* Empty State */}
            {/* ================================= */}

            {!loading &&
                !error &&
                interviews.length === 0 && (

                    <div className="history-empty">

                        <div className="history-empty-icon">
                            📝
                        </div>

                        <h2>
                            No Interviews Yet
                        </h2>

                        <p>
                            Your completed interviews will
                            appear here.
                        </p>

                    </div>

                )
            }


            {/* ================================= */}
            {/* Interview Cards */}
            {/* ================================= */}

            {!loading &&
                interviews.length > 0 && (

                    <div className="history-list">

                        <div className="history-count">

                            <span>
                                {interviews.length}
                            </span>

                            interview
                            {interviews.length !== 1
                                ? "s"
                                : ""
                            }

                        </div>


                        {interviews.map(
                            (interview) => (

                                <div
                                    className="history-card"
                                    key={
                                        interview.interview_id
                                    }
                                >


                                    {/* Card Header */}

                                    <div className="history-card-header">

                                        <div className="history-role">

                                            <div className="role-icon">
                                                💼
                                            </div>

                                            <div>

                                                <h2>
                                                    {
                                                        interview.job_role
                                                    }
                                                </h2>

                                                <span>
                                                    Interview #
                                                    {
                                                        interview.interview_id
                                                    }
                                                </span>

                                            </div>

                                        </div>


                                        <span
                                            className={
                                                interview.completed_at
                                                    ? "status-badge completed"
                                                    : "status-badge progress"
                                            }
                                        >

                                            {interview.completed_at
                                                ? "✓ Completed"
                                                : "● In Progress"
                                            }

                                        </span>

                                    </div>


                                    {/* Card Details */}

                                    <div className="history-details">


                                        <div className="history-detail">

                                            <span className="detail-icon">
                                                🎯
                                            </span>

                                            <div>

                                                <small>
                                                    Difficulty
                                                </small>

                                                <strong>
                                                    {
                                                        interview.difficulty
                                                    }
                                                </strong>

                                            </div>

                                        </div>


                                        <div className="history-detail">

                                            <span className="detail-icon">
                                                🧠
                                            </span>

                                            <div>

                                                <small>
                                                    Interview Type
                                                </small>

                                                <strong>
                                                    {
                                                        interview.interview_type
                                                    }
                                                </strong>

                                            </div>

                                        </div>


                                        <div className="history-detail">

                                            <span className="detail-icon">
                                                📅
                                            </span>

                                            <div>

                                                <small>
                                                    Started
                                                </small>

                                                <strong>
                                                    {
                                                        interview.started_at
                                                    }
                                                </strong>

                                            </div>

                                        </div>

                                    </div>


                                    {/* Card Footer */}

                                    <div className="history-card-footer">

                                        {interview.completed_at ? (

                                            <>

                                                <span className="completed-text">
                                                    ✓ Interview completed
                                                </span>


                                                <button
                                                    className="view-result-button"
                                                    onClick={() =>
                                                        viewResult(
                                                            interview.interview_id
                                                        )
                                                    }
                                                >
                                                    📊 View Result →
                                                </button>

                                            </>

                                        ) : (

                                            <span className="progress-text">
                                                ⏳ Interview in progress
                                            </span>

                                        )}

                                    </div>

                                </div>

                            )
                        )}

                    </div>

                )
            }


            {/* ================================= */}
            {/* Result Loading */}
            {/* ================================= */}

            {resultLoading && (

                <div className="result-loading-card">

                    <div className="history-spinner"></div>

                    <p>
                        Loading interview result...
                    </p>

                </div>

            )}


            {/* ================================= */}
            {/* Selected Result */}
            {/* ================================= */}

            {selectedResult && (

                <div className="history-result">


                    {/* Result Header */}

                    <div className="history-result-header">

                        <div className="result-history-icon">
                            🏆
                        </div>

                        <div>

                            <p>
                                INTERVIEW RESULT
                            </p>

                            <h2>
                                {
                                    selectedResult
                                        .interview
                                        .job_role
                                }
                            </h2>

                        </div>


                        <button
                            className="close-result-button"
                            onClick={() =>
                                setSelectedResult(null)
                            }
                        >
                            ✕
                        </button>

                    </div>


                    {/* Statistics */}

                    <div className="history-result-section">

                        <p className="result-section-label">
                            INTERVIEW SUMMARY
                        </p>

                        <h3>
                            Statistics
                        </h3>


                        <div className="history-stat-grid">


                            <div className="history-stat-card">

                                <span>
                                    📋
                                </span>

                                <strong>
                                    {
                                        selectedResult
                                            .statistics
                                            .total_questions
                                    }
                                </strong>

                                <small>
                                    Total Questions
                                </small>

                            </div>


                            <div className="history-stat-card">

                                <span>
                                    ✓
                                </span>

                                <strong>
                                    {
                                        selectedResult
                                            .statistics
                                            .answered_questions
                                    }
                                </strong>

                                <small>
                                    Answered
                                </small>

                            </div>


                            <div className="history-stat-card">

                                <span>
                                    🤖
                                </span>

                                <strong>
                                    {
                                        selectedResult
                                            .statistics
                                            .evaluated_questions
                                    }
                                </strong>

                                <small>
                                    Evaluated
                                </small>

                            </div>

                        </div>

                    </div>


                    {/* Scores */}

                    <div className="history-result-section">

                        <p className="result-section-label">
                            AI PERFORMANCE
                        </p>

                        <h3>
                            Performance Scores
                        </h3>


                        <div className="history-score-grid">


                            <div className="history-score-card">

                                <span>
                                    🎯
                                </span>

                                <small>
                                    Relevance
                                </small>

                                <strong>
                                    {
                                        selectedResult
                                            .scores
                                            .average_relevance_score
                                    }
                                </strong>

                                <em>
                                    / 100
                                </em>

                            </div>


                            <div className="history-score-card">

                                <span>
                                    🔑
                                </span>

                                <small>
                                    Keywords
                                </small>

                                <strong>
                                    {
                                        selectedResult
                                            .scores
                                            .average_keyword_score
                                    }
                                </strong>

                                <em>
                                    / 100
                                </em>

                            </div>


                            <div className="history-score-card">

                                <span>
                                    🧠
                                </span>

                                <small>
                                    Semantic
                                </small>

                                <strong>
                                    {
                                        selectedResult
                                            .scores
                                            .average_semantic_score
                                    }
                                </strong>

                                <em>
                                    / 100
                                </em>

                            </div>


                            <div className="history-score-card">

                                <span>
                                    ✨
                                </span>

                                <small>
                                    Clarity
                                </small>

                                <strong>
                                    {
                                        selectedResult
                                            .scores
                                            .average_clarity_score
                                    }
                                </strong>

                                <em>
                                    / 100
                                </em>

                            </div>

                        </div>

                    </div>


                    {/* Overall Score */}

                    <div className="history-overall">

                        <div>

                            <p>
                                OVERALL SCORE
                            </p>

                            <strong>
                                {
                                    selectedResult
                                        .scores
                                        .overall_score
                                }

                                <span>
                                    / 100
                                </span>
                            </strong>

                        </div>


                        <span className="history-performance">

                            {
                                selectedResult
                                    .scores
                                    .overall_score >= 85
                                    ? "Excellent! 🌟"
                                    : selectedResult
                                        .scores
                                        .overall_score >= 70
                                        ? "Good! 👍"
                                        : selectedResult
                                            .scores
                                            .overall_score >= 50
                                            ? "Keep improving! 💪"
                                            : "Keep practicing! 🚀"
                            }

                        </span>

                    </div>


                    {/* Feedback */}

                    <div className="history-feedback">

                        <div className="history-feedback-icon">
                            💡
                        </div>


                        <div>

                            <p>
                                AI FEEDBACK
                            </p>

                            <h3>
                                Personalized Feedback
                            </h3>

                            <span>
                                {
                                    selectedResult.feedback
                                }
                            </span>

                        </div>

                    </div>

                </div>

            )}

        </div>
    );
}


export default InterviewHistory;

