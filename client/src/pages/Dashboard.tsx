import './Dashboard.css';

function Dashboard() {
    return (
        <div className="dashboard">
            <div className='dashboard-content'>
                <div>
                    <h1 className="hero-title">
                        Welcome <span className="red-text">User</span>,<br />
                    </h1>
                    <input type="spending" className="input" placeholder="Product" />
                    <input type="cost" className="input" placeholder="Price" />
                    <button className="primary-btn">+</button>
                </div>
                <div className="table-section">
                    <div className='owe-you'>
                        <h2 className="table-title">They Owe You</h2>
                        <div className="debt-list">
                            <div className="debt-item">
                                <div className="debt-info">
                                    <span className="debt-person">John Doe</span>
                                    <span className="debt-reason">Pizza</span>
                                </div>
                                <div className="debt-info">
                                    <span className="debt-amount">$15.00</span>
                                    <button className="primary-btn">It's ok</button>
                                </div>
                            </div>
                            <div className="debt-item">
                                <div className="debt-info">
                                    <span className="debt-person">Alice Smith</span>
                                    <span className="debt-reason">Movie tickets</span>
                                </div>
                                <div className="debt-info">
                                    <span className="debt-amount">$25.00</span>
                                    <button className="primary-btn">It's ok</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className='you-owe'>
                        <h2 className="table-title">You Owe Them</h2>
                        <div className="debt-list">
                            <div className="debt-item">
                                <div className="debt-info">
                                    <span className="debt-person">Bob Johnson</span>
                                    <span className="debt-reason">Lunch</span>
                                    <span className="debt-amount">$12.50</span>
                                </div>
                                <button className="primary-btn">Done</button>
                            </div>
                            <div className="debt-item">
                                <div className="debt-info">
                                    <span className="debt-person">Sarah Wilson</span>
                                    <span className="debt-reason">Coffee</span>
                                    <span className="debt-amount">$5.00</span>
                                </div>
                                <button className="primary-btn">Done</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;