import "./DebtTable.css";
import type { Person } from "../types/interfaces";
import DebtItem from "./DebtItem";
import { useState } from "react";
import { categories } from "../constants/categories";
import type { HistoryActivity } from "../types/interfaces";

interface DebtTableProps {
  title: string;
  value: number;
  debts: (Person | HistoryActivity)[];
  status: "youOwe" | "history" | "theyOwe";
  onResolve?: (person: string, reason: string, amount: string) => void;
}

const DebtTable = ({ title, value, debts, status, onResolve }: DebtTableProps) => {
  const [selectedCategory, setSelectedCategory] = useState("All");
  const filteredDebts = debts.filter(debt => 
    selectedCategory === "All" || debt.category === selectedCategory
  );
  return (
    <div className={status === "history" ? "history" : "debt-table"}>
      <div className="table-header">
        <h2 className="table-title">
          {title} ${value}
        </h2>
        <select
        value={selectedCategory}
        onChange={(e) => setSelectedCategory(e.target.value)}>
          {categories.map((category) => (
            <option 
            key={category} 
            value={category}
            >
              {category}
            </option>
          ))}
        </select>
      </div>
      <div className="debt-list">
        {filteredDebts.map((debt) => (
          <DebtItem
            {...(status === "history" 
              ? {
                  reason: debt.reason,
                  amount: debt.amount,
                  status: status,
                  category: debt.category
                }
              : {
                  person: (debt as Person).person,
                  reason: debt.reason,
                  amount: debt.amount,
                  status: status,
                  category: debt.category,
                  resolved: (debt as Person).resolved,
                  onResolve: onResolve
                }
            )}
          />
        ))}
      </div>
    </div>
  );
};

export default DebtTable;