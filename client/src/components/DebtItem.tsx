import { useState } from "react";
import "./DebtItem.css";

interface DebtItemProps {
    person?: string;
    reason: string;  // название расхода или причина долга
    amount: string;  // сумма с валютой, например "1000 EUR"
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

    // Отобразить категорию, вне зависимости от типа (string или объект)
    const displayCategory = typeof category === "object" && category !== null
        ? category.name
        : category;

    // Отдельный рендер для истории
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

    // Для "You owe them"
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

    // Для "They owe you"
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
