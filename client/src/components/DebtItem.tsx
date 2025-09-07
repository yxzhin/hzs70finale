import { useState } from "react";
import "./DebtItem.css";

interface DebtItemProps {
  person?: string;
  reason: string;
  amount: string;
  category: string;
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
  }
  // The card for the "History" section
  if (status === "history") {
    return (
      <div className="debt-item">
        <div className="debt-info">
          <span className="debt-primary">{reason}</span>
          <span className="debt-secondary">- {category}</span>
        </div>
        <div className="debt-info">
          <span className="debt-amount">{amount}</span>
        </div>
      </div>
    );
  }
  // The card for the "You owe them" section
  // The next 2 cards can be edited so that the button action changes based on the status along with the button text
  if (status === "youOwe") {
    return (
      <div className="debt-item">
        <div className="debt-info">
          <span className="debt-primary">{person}</span>
          <span className="debt-secondary">{reason} - {category}</span>
        </div>
        <div className="debt-info">
          <span className="debt-amount">{amount}</span>
          {!resolved ? <button className="primary-btn" onClick={handleResolve}>Done</button> : <span className="checkmark">✓</span>}
        </div>
      </div>
    );
  }
  // The card for the "They owe you" section
  return (
    <div className="debt-item">
      <div className="debt-info">
        <span className="debt-primary">{person}</span>
        <span className="debt-secondary">{reason} - {category}</span>
      </div>
      <div className="debt-info">
        <span className="debt-amount">{amount}</span>
        {!resolved ? <button className="primary-btn" onClick={handleResolve}>Forgive</button> : <span className="checkmark">✓</span>}
      </div>
    </div>
  );
};

export default DebtItem;
