import { useMemo, useState } from 'react'

type Website = 'Amazon' | 'eBay' | 'Walmart' | 'Etsy' | 'AliExpress'
type DataField =
  | 'title'
  | 'price'
  | 'rating'
  | 'reviews_count'
  | 'product_url'
  | 'product_image'
  | 'seller'
  | 'availability'
type OutputFormat = 'table' | 'csv' | 'json' | 'excel' | 'pdf'
type JobStatus = 'queued' | 'running' | 'completed' | 'failed'

type JobResponse = {
  id: string
  status: JobStatus
  results: Array<Record<string, string | null>>
  error: string | null
}

const websites: Website[] = ['Amazon', 'eBay', 'Walmart', 'Etsy', 'AliExpress']
const fields: { label: string; value: DataField }[] = [
  { label: 'Product title', value: 'title' },
  { label: 'Price', value: 'price' },
  { label: 'Rating', value: 'rating' },
  { label: 'Number of reviews', value: 'reviews_count' },
  { label: 'Product URL', value: 'product_url' },
  { label: 'Product image', value: 'product_image' },
  { label: 'Seller/store name', value: 'seller' },
  { label: 'Availability/shipping info', value: 'availability' },
]
const outputFormats: OutputFormat[] = ['table', 'csv', 'json', 'excel', 'pdf']

const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

async function pollJob(jobId: string): Promise<JobResponse> {
  while (true) {
    const response = await fetch(`${apiBase}/jobs/${jobId}`)
    if (!response.ok) throw new Error('Unable to fetch scrape status')
    const job = (await response.json()) as JobResponse
    if (job.status === 'completed' || job.status === 'failed') return job
    await new Promise((resolve) => setTimeout(resolve, 900))
  }
}

function App() {
  const [selectedWebsites, setSelectedWebsites] = useState<Website[]>(['Amazon'])
  const [query, setQuery] = useState('wireless gaming mouse')
  const [selectedFields, setSelectedFields] = useState<DataField[]>(['title', 'price', 'product_url'])
  const [outputFormat, setOutputFormat] = useState<OutputFormat>('table')
  const [status, setStatus] = useState<JobStatus | 'idle'>('idle')
  const [results, setResults] = useState<Array<Record<string, string | null>>>([])
  const [error, setError] = useState<string>('')
  const [lastJobId, setLastJobId] = useState<string>('')

  const columns = useMemo(() => ['website', ...selectedFields], [selectedFields])

  const toggleWebsite = (website: Website) => {
    setSelectedWebsites((current) =>
      current.includes(website) ? current.filter((item) => item !== website) : [...current, website],
    )
  }

  const toggleField = (field: DataField) => {
    setSelectedFields((current) =>
      current.includes(field) ? current.filter((item) => item !== field) : [...current, field],
    )
  }

  const submit = async () => {
    setError('')
    setResults([])

    if (!selectedWebsites.length || !selectedFields.length || query.trim().length < 2) {
      setError('Please select at least one website, one field, and a valid search keyword.')
      return
    }

    setStatus('queued')

    try {
      const response = await fetch(`${apiBase}/scrape`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          websites: selectedWebsites,
          query,
          fields: selectedFields,
          output_format: outputFormat,
          max_pages: 2,
        }),
      })

      if (!response.ok) {
        throw new Error('Scrape submission failed')
      }

      const payload = (await response.json()) as { job_id: string }
      setLastJobId(payload.job_id)
      setStatus('running')

      const completedJob = await pollJob(payload.job_id)
      setStatus(completedJob.status)

      if (completedJob.status === 'failed') {
        setError(completedJob.error ?? 'Scrape failed')
      } else {
        setResults(completedJob.results)
      }
    } catch (submitError) {
      setStatus('failed')
      setError(submitError instanceof Error ? submitError.message : 'Unexpected scrape error')
    }
  }

  const download = async (format: Exclude<OutputFormat, 'table'>) => {
    if (!lastJobId) return
    const response = await fetch(`${apiBase}/jobs/${lastJobId}/export?output_format=${format}`)
    if (!response.ok) {
      setError('Export failed. Ensure the scrape job has completed.')
      return
    }

    const blob = await response.blob()
    const extensionMap: Record<string, string> = {
      csv: 'csv',
      json: 'json',
      excel: 'xlsx',
      pdf: 'pdf',
    }

    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `scrape-results.${extensionMap[format]}`
    link.click()
    URL.revokeObjectURL(link.href)
  }

  return (
    <main className="mx-auto w-full max-w-6xl p-4 md:p-8">
      <div className="rounded-xl bg-white p-6 shadow">
        <h1 className="m-0 text-2xl font-semibold md:text-3xl">E-Commerce Product Scraper</h1>
        <p className="mt-2 text-sm text-slate-600">Select websites, choose fields, run scrape, and export results.</p>

        <section className="mt-6 grid gap-6 md:grid-cols-2">
          <div>
            <label className="mb-2 block text-sm font-medium">Product keyword</label>
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              className="w-full rounded border border-slate-300 p-2"
              placeholder="wireless gaming mouse"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium">Output format</label>
            <select
              value={outputFormat}
              onChange={(event) => setOutputFormat(event.target.value as OutputFormat)}
              className="w-full rounded border border-slate-300 p-2"
            >
              {outputFormats.map((format) => (
                <option key={format} value={format}>
                  {format.toUpperCase()}
                </option>
              ))}
            </select>
          </div>
        </section>

        <section className="mt-6 grid gap-6 md:grid-cols-2">
          <div>
            <h2 className="mb-2 text-sm font-medium">Supported websites</h2>
            <div className="grid grid-cols-2 gap-2">
              {websites.map((website) => (
                <label key={website} className="flex items-center gap-2 rounded border border-slate-200 p-2 text-sm">
                  <input type="checkbox" checked={selectedWebsites.includes(website)} onChange={() => toggleWebsite(website)} />
                  {website}
                </label>
              ))}
            </div>
          </div>

          <div>
            <h2 className="mb-2 text-sm font-medium">Data fields</h2>
            <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
              {fields.map((field) => (
                <label key={field.value} className="flex items-center gap-2 rounded border border-slate-200 p-2 text-sm">
                  <input
                    type="checkbox"
                    checked={selectedFields.includes(field.value)}
                    onChange={() => toggleField(field.value)}
                  />
                  {field.label}
                </label>
              ))}
            </div>
          </div>
        </section>

        <div className="mt-6 flex flex-wrap items-center gap-3">
          <button onClick={submit} className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
            Run Scrape
          </button>

          {status !== 'idle' && (
            <span className="rounded bg-slate-100 px-3 py-1 text-sm">Status: {status}</span>
          )}

          {error && <span className="text-sm text-red-600">{error}</span>}
        </div>
      </div>

      {results.length > 0 && (
        <section className="mt-6 rounded-xl bg-white p-6 shadow">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <h2 className="m-0 text-xl font-semibold">Results ({results.length})</h2>
            <div className="flex gap-2">
              <button onClick={() => download('csv')} className="rounded border px-3 py-1 text-sm">
                Download CSV
              </button>
              <button onClick={() => download('json')} className="rounded border px-3 py-1 text-sm">
                Download JSON
              </button>
              <button onClick={() => download('excel')} className="rounded border px-3 py-1 text-sm">
                Download Excel
              </button>
              <button onClick={() => download('pdf')} className="rounded border px-3 py-1 text-sm">
                Download PDF
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full min-w-[700px] border-collapse text-left text-sm">
              <thead>
                <tr className="bg-slate-100">
                  {columns.map((column) => (
                    <th key={column} className="border border-slate-200 p-2 font-medium">
                      {column}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {results.map((row, index) => (
                  <tr key={`${row.website}-${index}`}>
                    {columns.map((column) => (
                      <td key={column} className="border border-slate-200 p-2 align-top">
                        {row[column] ?? '-'}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </main>
  )
}

export default App
