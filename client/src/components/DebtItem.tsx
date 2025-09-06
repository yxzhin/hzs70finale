import React from "react";
import "./DebtItem.css";

interface DebtItemProps {
  person: string;
  reason: string;
  amount: string;
  status?: "youOwe" | "history" | "theyOwe";
}

const DebtItem = (props: DebtItemProps) => {
  const { person, reason, amount, status } = props;
  if (status === "history") {
    return (
      <div className="debt-item">
        <div className="debt-info">
          <span className="debt-person">{person}</span>
          <span className="debt-reason">{reason}</span>
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
          <span className="debt-person">{person}</span>
          <span className="debt-reason">{reason}</span>
        </div>
        <div className="debt-info">
          <span className="debt-amount">{amount}</span>
          <button className="primary-btn">Done</button>
        </div>
      </div>
    );
  }
  return (
    <div className="debt-item">
        <div className="debt-info">
          <span className="debt-person">{person}</span>
          <span className="debt-reason">{reason}</span>
        </div>
        <div className="debt-info">
          <span className="debt-amount">{amount}</span>
          <button className="primary-btn">It's ok</button>
        </div>
      </div>
    );
};

export default DebtItem;
