function FloatingCard({
  className,
  label,
  value,
  description,
  status = false,
}) {
  return (
    <div className={`float-card ${className}`}>
      <div className="card-label">
        {status && <span className="green-dot"></span>}
        {label}
      </div>

      <strong>{value}</strong>

      <small>{description}</small>
    </div>
  );
}

export default FloatingCard;