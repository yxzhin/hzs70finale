import { useState } from "react";
import "./DebtItem.css";

interface DebtItemProps {
    person?: string;
    reason: string;
    amount: string;
    category: string | { name: string };
    status?: "youOwe" | "history" | "theyOwe";
    resolved?: boolean;
    onResolve?: (person: string, reason: string, amount: string) => void;
}

const DebtItem = (props: DebtItemProps) => {
    const { person, reason, amount, category, status, resolved, onResolve } = props;

    const handleResolve = () => {
        if (onResolve && person) {
            onResolve(person, reason, amount);
        }
    };

    const displayCategory = typeof category === 'object' && category !== null
        ? category.name
        : category;

    if (status === "history") {
        return (
            <div className="debt-item">
                <div className="debt-info">
                    <span className="debt-primary">{reason}</span>
                    <span className="debt-secondary">- {displayCategory}</span>
                </div>
                <div className="debt-info">
                    <span className="debt-amount">{amount}</span>
                </div>
            </div>
        );
    }

    if (status === "youOwe") {
        return (
            <div className="debt-item">
                <div className="debt-info">
                    <span className="debt-primary">{person}</span>
                    <span className="debt-secondary">{reason} - {displayCategory}</span>
                </div>
                <div className="debt-info">
                    <span className="debt-amount">{amount}</span>
                    {!resolved ? (
                        <button className="primary-btn" onClick={handleResolve}>
                            Done
                        </button>
                    ) : (
                        <span className="checkmark">✓</span>
                    )}
                </div>
            </div>
        );
    }

    return (
        <div className="debt-item">
            <div className="debt-info">
                <span className="debt-primary">{person}</span>
                <span className="debt-secondary">{reason} - {displayCategory}</span>
            </div>
            <div className="debt-info">
                <span className="debt-amount">{amount}</span>
                {!resolved ? (
                    <button className="primary-btn" onClick={handleResolve}>
                        Forgive
                    </button>
                ) : (
                    <span className="checkmark">✓</span>
                )}
            </div>
        </div>
    );
};

export default DebtItem;
