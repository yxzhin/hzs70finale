import "./Dashboard.css";
import DebtItem from "../components/DebtItem";

function Dashboard() {
  return (
    <div className="dashboard">
      <div className="dashboard-content">
        <div className="dashboard-header">
          <div className="dashboard-header-left">
            <h1 className="dashboard-title">
              Welcome <span className="red-text">User</span>,<br />
            </h1>
            <input type="spending" className="input" placeholder="Product" />
            <input type="cost" className="input" placeholder="Price" />
            <button className="primary-btn">+</button>
          </div>
          <div className="dashboard-header-right">
            <button className="secondary-btn">Leave</button>
            <button className="secondary-btn">Add Friend</button>
          </div>
        </div>
        <div className="table-section">
          <div className="they-owe">
            <h2 className="table-title">They Owe You</h2>
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
            <h2 className="table-title">You Owe Them</h2>
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
            <h2 className="table-title">History</h2>
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
    </div>
  );
}

export default Dashboard;
