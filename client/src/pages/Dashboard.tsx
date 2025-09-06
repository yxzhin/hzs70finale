import "./Dashboard.css";
import DebtItem from "../components/DebtItem";
import SplitOverlay from "../components/SplitOverlay";
import { useState } from "react";

function Dashboard() {
    const groupId = 123;

    const [isOverlayOpen, setIsOverlayOpen] = useState(false);
    let theyOweValue = "$40.00";
    let youOweValue = "$17.50";
    let historyValue = "$40.00";
    return (
        <div className="dashboard">
            <div className="dashboard-content">
                <h1 className="small-screen-welcome">
                    Welcome,
                    <br />
                    <span className="red-text">User</span>
                </h1>
                <div className="dashboard-header">
                    <div className="dashboard-header-left">
                        <h1 className="dashboard-title">
                            Welcome, <span className="red-text">User</span>
                        </h1>
                        <div className="add-spending-section">
                            <h1 className="dashboard-title">Add a spending</h1>
                            <button
                                className="primary-btn"
                                onClick={() => setIsOverlayOpen(true)}
                            >
                                +
                            </button>
                        </div>
                    </div>
                    <div className="dashboard-header-right">
                        <button className="primary-btn">Leave</button>
                        <a href={`/invite?id=${groupId}`}>
                            <button className="primary-btn">Add Friend</button>
                        </a>
                    </div>
                </div>
                <div className="table-section table-section-split">
                    <div className="they-owe">
                        <h2 className="table-title">
                            They Owe You {theyOweValue}
                        </h2>
                        <div className="debt-list">
                            <DebtItem
                                person="John Doe"
                                reason="Pizza"
                                amount="$15.00"
                                status="theyOwe"
                            />
                            <DebtItem
                                person="Alice Smith"
                                reason="Movie tickets"
                                amount="$25.00"
                                status="theyOwe"
                            />
                        </div>
                    </div>

                    <div className="you-owe">
                        <h2 className="table-title">
                            You Owe Them {youOweValue}
                        </h2>
                        <div className="debt-list">
                            <DebtItem
                                person="Bob Johnson"
                                reason="Lunch"
                                amount="$12.50"
                                status="youOwe"
                            />
                            <DebtItem
                                person="Sarah Wilson"
                                reason="Coffee"
                                amount="$5.00"
                                status="youOwe"
                            />
                        </div>
                    </div>
                </div>
                <div className="table-section">
                    <div className="history">
                        <h2 className="table-title">
                            Group history: spent {historyValue} together
                        </h2>
                        <div className="debt-list">
                            <DebtItem
                                person="John Doe"
                                reason="Pizza"
                                amount="$15.00"
                                status="history"
                            />
                            <DebtItem
                                person="Alice Smith"
                                reason="Movie tickets"
                                amount="$25.00"
                                status="history"
                            />
                        </div>
                    </div>
                </div>
            </div>
            <SplitOverlay
                isOpen={isOverlayOpen}
                onClose={() => setIsOverlayOpen(false)}
                onApply={(data) => {
                    console.log("Split data:", data);
                    setIsOverlayOpen(false);
                    // Here you would handle the split data
                }}
            />
        </div>
    );
}

export default Dashboard;
