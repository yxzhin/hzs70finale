import "./Dashboard.css";
import SplitOverlay from "../components/SplitOverlay";
import { useState } from "react";
import DebtTable from "../components/DebtTable";
import type { Person } from "../types/interfaces";
import type { HistoryActivity } from "../types/interfaces";

function Dashboard() {
    const groupId = 123;
    // Replace these with actual data fetching logic
    const theyOweList = [
        { person: "John Doe", reason: "Pizza", amount: "$15.00", category: "Food" },
        { person: "Alice Smith", reason: "Movie tickets", amount: "$25.00", category: "Entertainment" },
    ];
    const youOweList = [
        { person: "Bob Johnson", reason: "Lunch", amount: "$12.50", category: "Food" },
        { person: "Sarah Wilson", reason: "Coffee", amount: "$5.00", category: "Food" },
    ];
    const historyList = [
        { reason: "Pizza", amount: "$15.00", category: "Food" },
        { reason: "Movie tickets", amount: "$25.00", category: "Entertainment" },
    ];
    const [theyOwe, setTheyOwe] = useState<Person[]>(theyOweList);
    const [youOwe, setYouOwe] = useState<Person[]>(youOweList);
    const [history, setHistory] = useState<HistoryActivity[]>(historyList);
    const [isOverlayOpen, setIsOverlayOpen] = useState(false);
    const youOweValue = youOweList.reduce((total, currentItem) => { const amount = parseFloat(currentItem.amount.replace('$', '')); return total + amount; }, 0);
    const historyValue = historyList.reduce((total, currentItem) => { const amount = parseFloat(currentItem.amount.replace('$', '')); return total + amount; }, 0)
    const theyOweValue = theyOweList.reduce((total, currentItem) => { const amount = parseFloat(currentItem.amount.replace('$', '')); return total + amount; }, 0);
    // Here we should add the logic for removing debt from the server
    const handleDebtResolution = (person: string, reason: string, amount: string) => {
        // Add to history
        /*setHistory(prev => [...prev, { reason, amount, category: "Food" }]);*/

        // Remove from respective list
        if (theyOwe.some(debt => debt.person === person)) {
            setTheyOwe(prev => prev.filter(debt => debt.person !== person));
        } else {
            setYouOwe(prev => prev.filter(debt => debt.person !== person));
        }
    };
    const userId = localStorage.getItem('userid');
    return (
        <div className="dashboard">
            <div className="dashboard-content">
                <h1 className="small-screen-welcome">
                    Welcome,
                    <br />
                    <span className="red-text">{userId}</span>
                </h1>
                <div className="dashboard-header">
                    <div className="dashboard-header-left">
                        <h1 className="dashboard-title">
                            Welcome, <span className="red-text">{userId}</span>
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
                    <DebtTable
                        title="They Owe You"
                        value={theyOweValue}
                        debts={theyOwe}
                        status="theyOwe"
                        onResolve={handleDebtResolution}
                    />
                    <DebtTable
                        title="You Owe Them"
                        value={youOweValue}
                        debts={youOwe}
                        status="youOwe"
                        onResolve={handleDebtResolution}
                    />
                </div>
                <div className="table-section">
                    <DebtTable
                        title="Group history: spent"
                        value={historyValue}
                        debts={history}
                        status="history"
                    />
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
