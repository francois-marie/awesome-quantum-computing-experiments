import { useMemo, useState } from 'react';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel,
  useReactTable,
  type SortingState,
} from '@tanstack/react-table';
import { ArrowDown, ArrowUp, ArrowUpDown, ExternalLink } from 'lucide-react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { platformColor, type Row } from '@/lib/data';
import { cn } from 'cn';

interface Props {
  rows: Row[];
  columns: string[];
  /** Columns shown by default; the rest are available under "more columns". */
  primary: string[];
  initialSort?: string;
}

const HIDDEN = new Set(['Link', 'Article Title', 'First Author']);

function PlatformCell({ value }: { value: string }) {
  if (!value) return null;
  return (
    <span className="inline-flex items-center gap-1.5 whitespace-nowrap">
      <span className="inline-block size-2 rounded-full" style={{ background: platformColor(value) }} />
      {value}
    </span>
  );
}

const compare = (a: string, b: string) => {
  const na = Number(a);
  const nb = Number(b);
  if (a !== '' && b !== '' && Number.isFinite(na) && Number.isFinite(nb)) return na - nb;
  if (a === '') return 1;
  if (b === '') return -1;
  return a.localeCompare(b);
};

export function DataTable({ rows, columns, primary, initialSort = 'Year' }: Props) {
  const [sorting, setSorting] = useState<SortingState>([{ id: initialSort, desc: true }]);
  const [filter, setFilter] = useState('');
  const [showAll, setShowAll] = useState(false);

  const cols = useMemo(() => {
    const helper = createColumnHelper<Row>();
    const visible = showAll ? columns.filter((c) => !HIDDEN.has(c)) : primary;
    const paper = helper.display({
      id: 'paper',
      header: 'Paper',
      cell: ({ row }) => {
        const r = row.original;
        return (
          <a href={r.Link} target="_blank" rel="noopener" className="group flex min-w-[18rem] max-w-[30rem] items-start gap-1 whitespace-normal hover:underline">
            <span>
              {r['Article Title']}
              {r['First Author'] && <span className="text-muted-foreground"> · {r['First Author']} et al.</span>}
            </span>
            <ExternalLink className="mt-0.5 size-3 shrink-0 opacity-0 transition-opacity group-hover:opacity-60" />
          </a>
        );
      },
    });
    return [
      paper,
      ...visible.map((c) =>
        helper.accessor((r) => r[c] ?? '', {
          id: c,
          header: c,
          sortingFn: (a, b) => compare(a.getValue<string>(c), b.getValue<string>(c)),
          cell: ({ getValue }) => {
            const v = getValue<string>();
            if (c === 'Platform') return <PlatformCell value={v} />;
            const long = v.length > 60;
            return <span className={cn(long ? 'block min-w-[16rem] max-w-[26rem] whitespace-normal text-xs text-muted-foreground' : 'whitespace-nowrap')}>{v}</span>;
          },
        }),
      ),
    ];
  }, [columns, primary, showAll]);

  const table = useReactTable({
    data: rows,
    columns: cols,
    state: { sorting, globalFilter: filter },
    onSortingChange: setSorting,
    onGlobalFilterChange: setFilter,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    globalFilterFn: (row, _col, value: string) => {
      const q = value.toLowerCase();
      return Object.values(row.original).some((v) => v.toLowerCase().includes(q));
    },
  });

  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-wrap items-center gap-2">
        <input
          type="search"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Filter rows…"
          className="h-8 w-64 rounded-md border bg-background px-2.5 text-sm outline-none focus:ring-2 focus:ring-ring/40"
        />
        <span className="text-xs text-muted-foreground tabular-nums">
          {table.getFilteredRowModel().rows.length} / {rows.length} rows
        </span>
        <button type="button" onClick={() => setShowAll((s) => !s)} className="ml-auto rounded-md border px-2.5 py-1 text-xs hover:bg-muted">
          {showAll ? 'Fewer columns' : 'All columns'}
        </button>
      </div>
      <div className="overflow-x-auto rounded-lg border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((hg) => (
              <TableRow key={hg.id}>
                {hg.headers.map((h) => {
                  const sorted = h.column.getIsSorted();
                  return (
                    <TableHead key={h.id} className="whitespace-nowrap">
                      {h.column.getCanSort() ? (
                        <button type="button" onClick={h.column.getToggleSortingHandler()} className="inline-flex items-center gap-1 font-medium hover:text-foreground">
                          {flexRender(h.column.columnDef.header, h.getContext())}
                          {sorted === 'asc' ? <ArrowUp className="size-3" /> : sorted === 'desc' ? <ArrowDown className="size-3" /> : <ArrowUpDown className="size-3 opacity-40" />}
                        </button>
                      ) : (
                        flexRender(h.column.columnDef.header, h.getContext())
                      )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.map((row) => (
              <TableRow key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id} className="align-top text-sm">
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
