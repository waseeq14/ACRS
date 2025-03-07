import { BrowserRouter as Router, Routes, Route } from 'react-router'
import Loading from './routes/Loading'
import Login from './routes/Login'
import Register from './routes/Register'
import Dashboard from './routes/Dashboard'
import DashboardHome from './routes/DashboardHome'
import VulnerabilityAssessment from './routes/VulnerabilityAssessment'
import RunKLEE from './routes/RunKLEE'
import RunKLEE2 from './routes/RunKLEE2'
import Fuzzer from './routes/Fuzzer'
import ExploitGeneration from './routes/ExploitGeneration'
import PatchSuggestion from './routes/PatchSuggestion'
import PentesterMode from './routes/PentesterMode'
import Reports from './routes/Reports'
import { AppProvider } from './context/AppContext'

import './App.css'

const navigationLinks = [
  {
    path: '',
    name: 'Dashboard'
  },
  {
    path: '/va',
    name: 'Vulnerability Assessment'
  },
  {
    path: '/va/klee',
    name: 'KLEE'
  },
  {
    path: '/va/advanced_klee',
    name: 'Priotize Code Paths',
  },
  {
    path: '/va/fuzzer',
    name: 'Fuzzer'
  },
  {
    path: '/exploit',
    name: 'Exploit Generation'
  },
  {
    path: '/patch',
    name: 'Patch Suggestion'
  },
  {
    path: '/pentester-mode',
    name: 'Pentester Mode'
  },
  {
    path: '/reports',
    name: 'Reports'
  }
]

function App() {
  return (
    <div className='App'>
      <AppProvider>
        <Router>
          <Routes>
            <Route index element={<Loading />} />
            <Route path='login' element={<Login />} />
            <Route path='create-account' element={<Register />} />
            <Route
              path='dashboard'
              element={<Dashboard navigationLinks={navigationLinks} />}
            >
              <Route index element={<DashboardHome />} />
              <Route path='va'>
                <Route index element={<VulnerabilityAssessment />} />
                <Route path='klee' element={<RunKLEE />} />
                <Route path='advanced_klee' element={<RunKLEE2 />} />
                <Route path='fuzzer' element={<Fuzzer />} />
              </Route>
              <Route path='exploit' element={<ExploitGeneration />} />
              <Route path='patch' element={<PatchSuggestion />} />
              <Route path='pentester-mode' element={<PentesterMode />} />
              <Route path='reports' element={<Reports />} />
            </Route>
          </Routes>
        </Router>
      </AppProvider>
    </div>
  )
}

export default App
