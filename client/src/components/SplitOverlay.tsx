import { useState, useEffect } from "react";
import "./SplitOverlay.css";

interface Person {
    name: string;
    isParticipating: boolean;
    paid: string;
    shouldPay: string;
}

interface SplitOverlayProps {
    isOpen: boolean;
    onClose: () => void;
    onApply: (data: any) => void;
}

function SplitOverlay({ isOpen, onClose, onApply }: SplitOverlayProps) {
    const [activity, setActivity] = useState("");
    const [totalAmount, setTotalAmount] = useState("");
    const [divideEqually, setDivideEqually] = useState(true);
    const [people, setPeople] = useState<Person[]>([
        { name: "John Doe", isParticipating: false, paid: "0", shouldPay: "0" },
        { name: "Alice Smith", isParticipating: false, paid: "0", shouldPay: "0" },
        { name: "Bob Johnson", isParticipating: false, paid: "0", shouldPay: "0" },
        { name: "Sarah Wilson", isParticipating: false, paid: "0", shouldPay: "0" },
    ]);
    const [totalPaid, setTotalPaid] = useState(0);
    const [isValid, setIsValid] = useState(false);
    const resetOverlay = () => {
        setActivity("");
        setTotalAmount("");
        setDivideEqually(true);
        setPeople([
            { name: "John Doe", isParticipating: false, paid: "0", shouldPay: "0" },
            {
                name: "Alice Smith",
                isParticipating: false,
                paid: "0",
                shouldPay: "0",
            },
            {
                name: "Bob Johnson",
                isParticipating: false,
                paid: "0",
                shouldPay: "0",
            },
            {
                name: "Sarah Wilson",
                isParticipating: false,
                paid: "0",
                shouldPay: "0",
            },
        ]);
        setTotalPaid(0);
        setIsValid(false);
    };
    const handleParticipantChange = (index: number, checked: boolean) => {
        const newPeople = [...people];
        newPeople[index].isParticipating = checked;
        if (!checked) {
            newPeople[index].paid = "0";
            newPeople[index].shouldPay = "0";
        }
        setPeople(newPeople);
    };
    const handleClose = () => {
        resetOverlay();
        onClose();
    };
    const handleApply = () => {
        onApply(people);
        resetOverlay();
        onClose();
    };
    useEffect(() => {
        if (divideEqually && totalAmount) {
            const participants = people.filter((p) => p.isParticipating).length;
            const perPerson = participants
                ? (parseFloat(totalAmount) / participants).toFixed(2)
                : "0";
            setPeople(
                people.map((person) => ({
                    ...person,
                    shouldPay: person.isParticipating ? perPerson : "0",
                }))
            );
        }
    }, [
        divideEqually,
        totalAmount,
        people.map((p) => p.isParticipating).join(","),
    ]);

    useEffect(() => {
        const total = people
            .filter((p) => p.isParticipating)
            .reduce((sum, person) => sum + parseFloat(person.paid || "0"), 0);
        setTotalPaid(total);
        // Add activity check to validation
        setIsValid(
            total === parseFloat(totalAmount || "0") &&
            total > 0 &&
            activity.trim() !== ""
        );
    }, [people, totalAmount, activity]); // Add activity to dependencies

    if (!isOpen) return null;

    return (
        <div className="overlay">
            <div className="overlay-content">
                <h2>Split Expense</h2>

                <div className="input-group">
                    <input
                        type="text"
                        placeholder="Activity (e.g., Pizza)"
                        value={activity}
                        onChange={(e) => setActivity(e.target.value)}
                        className="input"
                    />
                    <input
                        type="number"
                        placeholder="Total Amount"
                        value={totalAmount}
                        onChange={(e) => setTotalAmount(e.target.value)}
                        className="input"
                    />
                </div>

                <label className="checkbox-label">
                    <input
                        type="checkbox"
                        checked={divideEqually}
                        onChange={(e) => setDivideEqually(e.target.checked)}
                    />
                    Divide Equally
                </label>

                <table className="split-table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Paid</th>
                            <th>Should Pay</th>
                            <th>Overpaid/Not paid</th>
                        </tr>
                    </thead>
                    <tbody>
                        {people.filter((p) => p).map((person, index) => (
                            <tr key={index}>
                                <td className="check-name"><input
                                    type="checkbox"
                                    checked={person.isParticipating}
                                    onChange={(e) =>
                                        handleParticipantChange(index, e.target.checked)
                                    } />{person.name}</td>
                                <td>
                                    <input
                                        type="number"
                                        value={person.paid}
                                        onChange={(e) => {
                                            const newPeople = [...people];
                                            const personIndex = people.findIndex(
                                                (p) => p.name === person.name
                                            );
                                            newPeople[personIndex].paid = e.target.value;
                                            setPeople(newPeople);
                                        }}
                                        disabled={!person.isParticipating}
                                        className="input"
                                    />
                                </td>
                                <td>
                                    <input
                                        type="number"
                                        value={person.shouldPay}
                                        onChange={(e) => {
                                            if (!divideEqually) {
                                                const newPeople = [...people];
                                                const personIndex = people.findIndex(
                                                    (p) => p.name === person.name
                                                );
                                                newPeople[personIndex].shouldPay = e.target.value;
                                                setPeople(newPeople);
                                            }
                                        }}
                                        disabled={divideEqually}
                                        className="input"
                                    />
                                </td>
                                <td>
                                    <p>{parseFloat(person.paid) - parseFloat(person.shouldPay)}</p>
                                </td>
                            </tr>
                        ))}
                        <tr className="total-row">
                            <td>Total</td>
                            <td>${totalPaid.toFixed(2)}</td>
                            <td>${totalAmount || "0"}</td>
                        </tr>
                    </tbody>
                </table>

                <div className="button-group">
                    <button className="primary-btn" onClick={handleClose}>
                        Cancel
                    </button>
                    <button
                        className={`primary-btn ${!isValid ? "disabled" : ""}`}
                        onClick={handleApply}
                        disabled={!isValid}
                    >
                        Apply
                    </button>
                </div>
            </div>
        </div>
    );
}

export default SplitOverlay;

