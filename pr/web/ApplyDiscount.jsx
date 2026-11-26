import { useEffect, useState } from "react";

// Shown on the checkout page, under the order summary.
export default function ApplyDiscount({ cartId, total, onTotalChange }) {
  const [code, setCode] = useState("");
  const [message, setMessage] = useState("");
  const [suggested, setSuggested] = useState([]);

  // Codes we suggest to this customer, shown as buttons.
  useEffect(() => {
    fetch(`/api/checkout/suggested-codes?cartId=${cartId}`)
      .then((res) => res.json())
      .then((data) => setSuggested(data));
  });

  async function apply() {
    const res = await fetch("/api/checkout/discount", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cartId, code, total }),
    });
    const data = await res.json();
    setMessage(data.message);
    onTotalChange(data.total);
  }

  return (
    <div className="discount">
      <input value={code} onChange={(e) => setCode(e.target.value)} placeholder="Discount code" />
      <button onClick={apply}>Apply</button>
      {suggested.map((c) => (
        <button key={c} onClick={() => setCode(c)}>{c}</button>
      ))}
      <p dangerouslySetInnerHTML={{ __html: message }} />
    </div>
  );
}
