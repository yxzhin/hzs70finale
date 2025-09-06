import './Information.css';

function Information() {
    return (
        <div className="information">
            <div className="sec sec1">
                <div className="lside-sec">
                    <h1 className='title-info'>What is this app?</h1>
                    <p className='desc-info'>
                        SplitSmart is the easiest way for young people to share expenses with friends, roommates, or travel groups.
                        Instead of awkward money talks or endless spreadsheets, it keeps everything transparent by
                        tracking who paid what and calculating balances instantly.<br />
                        Whether you're splitting rent, utilities, groceries, or trip costs, the app makes sure everyone pays their fair share. With simple expense logging, instant balance updates, and quick settle-up options, managing shared money becomes stress-free and even fun. SplitSmart turns everyday bill-splitting into a smart financial habit.
                    </p>
                </div>

                <div className="rside-sec">
                    <img src="/pizza.jpg" className='img-info' />
                </div>
            </div>

            <div className="sec sec2">
                <div className="lside-sec">
                    <img src="/friends.png" className='img-info' />
                </div>

                <div className="rside-sec">
                    <h1 className='title-info'>What is this app?</h1>
                    <p className='desc-info'>
                        SplitSmart is the easiest way for young people to share expenses with friends, roommates, or travel groups.
                        Instead of awkward money talks or endless spreadsheets, it keeps everything transparent by
                        tracking who paid what and calculating balances instantly.<br />
                        Whether you're splitting rent, utilities, groceries, or trip costs, the app makes sure everyone pays their fair share. With simple expense logging, instant balance updates, and quick settle-up options, managing shared money becomes stress-free and even fun. SplitSmart turns everyday bill-splitting into a smart financial habit.
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Information;