export default function DataTable({ columns, rows }) {
  return (
    <div className="overflow-x-auto rounded-lg border border-beige/60 max-h-96 overflow-y-auto">
      <table className="min-w-full text-sm">
        <thead className="bg-beige sticky top-0">
          <tr>
            {columns.map((c) => (
              <th key={c} className="text-left font-semibold px-3 py-2 whitespace-nowrap">{c}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} className={i % 2 === 0 ? "bg-offwhite" : "bg-sand"}>
              {row.map((cell, j) => (
                <td key={j} className="px-3 py-1.5 whitespace-nowrap">
                  {cell === null || cell === undefined ? (
                    <span className="text-taupe">—</span>
                  ) : (
                    String(cell)
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
