import "./DebtItem.css";

interface DebtItemProps {
  person: string;
  reason: string;
  amount: string;
  status?: "youOwe" | "history" | "theyOwe";
}

const DebtItem = (props: DebtItemProps) => {
  const { person, reason, amount, status } = props;
  // The card for the "History" section
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
  // The card for the "You owe them" section
  // The next 2 cards can be edited so that the button action changes based on the status along with the button text
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
  // The card for the "They owe you" section
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
