import { useState } from "react";

import api from "../services/api";


function InterviewResult({ interview }) {

    const [result, setResult] = useState(null);

    const [message, setMessage] = useState("");

    const [error, setError] = useState("");

    const [loading, setLoading] = useState(false);


    /* ============================= */
    /* Complete Interview */
    /* ============================= */

    const completeInterview = async () => {

        setMessage("");
        setError("");
        setLoading(true);


        try {

            const response = await api.put(
                `/interviews/${interview.interview_id}/complete`
            );


            setMessage(
                response.data.message
            );


            await getResult();


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
    /* Get Result */
    /* ============================= */

    const getResult = async () => {

        try {

            const response = await api.get(
                `/interviews/${interview.interview_id}/result`
            );


            setResult(
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
        }
    };


    /* ============================= */
    /* No Interview */
    /* ============================= */

    if (!interview) {

        return (

            <div className="result-empty">

                <div className="result-empty-icon">
                    📊
                </div>

                <h2>
                    No Interview Selected
                </h2>

                <p>
                    Please select an interview to view
                    its result.
                </p>

            </div>

        );
    }


    return (

        <div className="interview-result-page">


            {/* ================================= */}
            {/* Header */}
            {/* ================================= */}

            <div className="result-header">

                <div className="result-header-icon">
                    🏆
                </div>


                <div>

                    <p className="result-header-label">
                        INTERVIEW REPORT
                    </p>

                    <h1>
                        {interview.job_role}
                    </h1>

                    <p>
                        Review your AI-powered interview
                        performance.
                    </p>

                </div>

            </div>


            {/* ================================= */}
            {/* Interview Information */}
            {/* ================================= */}

            <div className="result-info-row">

                <div className="result-info-card">

                    <span>
                        🎯
                    </span>

                    <div>

                        <small>
                            Difficulty
                        </small>

                        <strong>
                            {interview.difficulty}
                        </strong>

                    </div>

                </div>


                <div className="result-info-card">

                    <span>
                        💼
                    </span>

                    <div>

                        <small>
                            Interview Type
                        </small>

                        <strong>
                            {interview.interview_type}
                        </strong>

                    </div>

                </div>


                <div className="result-info-card">

                    <span>
                        🆔
                    </span>

                    <div>

                        <small>
                            Interview ID
                        </small>

                        <strong>
                            #{interview.interview_id}
                        </strong>

                    </div>

                </div>

            </div>


            {/* ================================= */}
            {/* Complete Interview */}
            {/* ================================= */}

            {!result && (

                <div className="complete-interview-card">

                    <div className="complete-icon">
                        🎓
                    </div>


                    <h2>
                        Ready to see your result?
                    </h2>


                    <p>
                        Complete your interview to calculate
                        your performance scores and receive
                        AI-powered feedback.
                    </p>


                    <button
                        className="complete-button"
                        onClick={completeInterview}
                        disabled={loading}
                    >

                        {loading ? (
                            <>
                                <span className="result-spinner"></span>
                                Completing Interview...
                            </>
                        ) : (
                            <>
                                ✓ Complete Interview
                            </>
                        )}

                    </button>

                </div>

            )}


            {/* ================================= */}
            {/* Messages */}
            {/* ================================= */}

            {message && (

                <div className="result-success">
                    ✓ {message}
                </div>

            )}


            {error && (

                <div className="result-error">
                    ⚠ {error}
                </div>

            )}


            {/* ================================= */}
            {/* Result */}
            {/* ================================= */}

            {result && (

                <div className="result-content">


                    {/* ================================= */}
                    {/* Overall Score */}
                    {/* ================================= */}

                    <div className="overall-result-card">

                        <div className="overall-result-icon">
                            ⭐
                        </div>


                        <div className="overall-result-text">

                            <p>
                                OVERALL PERFORMANCE
                            </p>

                            <h2>
                                {result.scores.overall_score}
                                <span>
                                    / 100
                                </span>
                            </h2>

                        </div>


                        <div className="performance-message">

                            {result.scores.overall_score >= 85
                                ? "Excellent Performance! 🌟"
                                : result.scores.overall_score >= 70
                                    ? "Good Performance! 👍"
                                    : result.scores.overall_score >= 50
                                        ? "Fair Performance. Keep improving! 💪"
                                        : "Keep practicing and improving! 🚀"
                            }

                        </div>

                    </div>


                    {/* ================================= */}
                    {/* Statistics */}
                    {/* ================================= */}

                    <div className="result-section-title">

                        <p>
                            INTERVIEW SUMMARY
                        </p>

                        <h2>
                            Your Statistics
                        </h2>

                    </div>


                    <div className="statistics-grid">

                        <div className="statistics-card">

                            <div className="statistics-icon blue">
                                📋
                            </div>

                            <div>

                                <strong>
                                    {result.statistics.total_questions}
                                </strong>

                                <span>
                                    Total Questions
                                </span>

                            </div>

                        </div>


                        <div className="statistics-card">

                            <div className="statistics-icon green">
                                ✓
                            </div>

                            <div>

                                <strong>
                                    {result.statistics.answered_questions}
                                </strong>

                                <span>
                                    Answered
                                </span>

                            </div>

                        </div>


                        <div className="statistics-card">

                            <div className="statistics-icon purple">
                                🤖
                            </div>

                            <div>

                                <strong>
                                    {result.statistics.evaluated_questions}
                                </strong>

                                <span>
                                    Evaluated
                                </span>

                            </div>

                        </div>

                    </div>


                    {/* ================================= */}
                    {/* Performance Scores */}
                    {/* ================================= */}

                    <div className="result-section-title">

                        <p>
                            AI PERFORMANCE ANALYSIS
                        </p>

                        <h2>
                            Performance Scores
                        </h2>

                    </div>


                    <div className="result-score-grid">


                        <div className="result-score-card">

                            <div className="result-score-icon">
                                🎯
                            </div>

                            <span>
                                Relevance
                            </span>

                            <strong>
                                {result.scores.average_relevance_score}
                            </strong>

                            <small>
                                / 100
                            </small>

                        </div>


                        <div className="result-score-card">

                            <div className="result-score-icon">
                                🔑
                            </div>

                            <span>
                                Keywords
                            </span>

                            <strong>
                                {result.scores.average_keyword_score}
                            </strong>

                            <small>
                                / 100
                            </small>

                        </div>


                        <div className="result-score-card">

                            <div className="result-score-icon">
                                🧠
                            </div>

                            <span>
                                Semantic
                            </span>

                            <strong>
                                {result.scores.average_semantic_score}
                            </strong>

                            <small>
                                / 100
                            </small>

                        </div>


                        <div className="result-score-card">

                            <div className="result-score-icon">
                                ✨
                            </div>

                            <span>
                                Clarity
                            </span>

                            <strong>
                                {result.scores.average_clarity_score}
                            </strong>

                            <small>
                                / 100
                            </small>

                        </div>

                    </div>


                    {/* ================================= */}
                    {/* AI Feedback */}
                    {/* ================================= */}

                    <div className="ai-feedback-result">

                        <div className="feedback-result-icon">
                            💡
                        </div>


                        <div>

                            <p>
                                AI FEEDBACK
                            </p>

                            <h2>
                                Personalized Feedback
                            </h2>

                            <div className="feedback-result-text">

                                {result.feedback}

                            </div>

                        </div>

                    </div>

                </div>

            )}

        </div>
    );
}


export default InterviewResult;

