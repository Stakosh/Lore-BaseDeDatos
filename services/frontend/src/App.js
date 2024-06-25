import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { Container, Row, Col } from 'react-bootstrap';
import Home from './Home';

import FilterSchools from './FilterSchools';

function App() {
  return (
    <Router>
      <Container>
        <Row className="my-4">
          <Col>
            <h1 className="text-center">Estadísticas de Escuelas</h1>
            <nav>
              <ul>
                <li><Link to="/">Inicio</Link></li>
                <li><Link to="/filter-schools">Filtrar Colegios</Link></li>
              </ul>
            </nav>
          </Col>
        </Row>
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route path="/filter-schools" element={<FilterSchools />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;
