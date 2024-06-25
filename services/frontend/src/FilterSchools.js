import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Row, Col, Card, Form, Button } from 'react-bootstrap';

function FilterSchools() {
  const [comuna, setComuna] = useState('');
  const [comunas, setComunas] = useState([]);
  const [schools, setSchools] = useState([]);
  const [filteredSchools, setFilteredSchools] = useState([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    // Fetch all comunas when the component mounts
    axios.get('http://localhost:5000/api/stats/all_comunas')
      .then(response => {
        setComunas(response.data.comunas);
      })
      .catch(error => console.error('Error fetching comunas:', error));
  }, []);

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.get('http://localhost:5000/api/stats/schools/filter', {
        params: { comuna: comuna }
      });
      setSchools(response.data.schools);
      setFilteredSchools(response.data.schools);  // Initially set filtered schools to all schools
    } catch (error) {
      console.error('Error fetching schools:', error);
    }
  };

  const handleFilter = () => {
    let filtered = schools;
    if (filter === 'worst_infrastructure') {
      filtered = schools.filter(school => school.Infraestructura === 'Mala');
    } else if (filter === 'best_infrastructure') {
      filtered = schools.filter(school => school.Infraestructura === 'Buena');
    } else if (filter === 'worst_teachers') {
      filtered = schools.filter(school => school.Preparacion_Maestros === 'Bajo');
    } else if (filter === 'best_teachers') {
      filtered = schools.filter(school => school.Preparacion_Maestros === 'Alto');
    }
    setFilteredSchools(filtered);
  };

  return (
    <Container>
      <Row className="my-4">
        <Col>
          <h1 className="text-center">Buscar Colegios por Comuna</h1>
        </Col>
      </Row>
      <Row className="my-4">
        <Col>
          <Form onSubmit={handleFormSubmit}>
            <Form.Group controlId="comuna">
              <Form.Label>Comuna</Form.Label>
              <Form.Control as="select" value={comuna} onChange={e => setComuna(e.target.value)}>
                <option value="">Selecciona una comuna</option>
                {comunas.map((comuna, index) => (
                  <option key={index} value={comuna}>{comuna}</option>
                ))}
              </Form.Control>
            </Form.Group>
            <Button variant="primary" type="submit" className="mt-3">
              Buscar
            </Button>
          </Form>
        </Col>
      </Row>
      {schools.length > 0 && (
        <>
          <Row className="my-4">
            <Col>
              <h2 className="text-center">Filtrar Resultados</h2>
              <Form>
                <Form.Group controlId="filter">
                  <Form.Label>Filtro</Form.Label>
                  <Form.Control as="select" value={filter} onChange={e => setFilter(e.target.value)}>
                    <option value="">Selecciona un filtro</option>
                    <option value="worst_infrastructure">Peor Infraestructura</option>
                    <option value="best_infrastructure">Mejor Infraestructura</option>
                    <option value="worst_teachers">Peores Profesores</option>
                    <option value="best_teachers">Mejores Profesores</option>
                  </Form.Control>
                </Form.Group>
                <Button variant="primary" onClick={handleFilter} className="mt-3">
                  Filtrar
                </Button>
              </Form>
            </Col>
          </Row>
          <Row>
            {filteredSchools.map(school => (
              <Col key={school.ID_Escuela} md={4} className="mb-4">
                <Card>
                  <Card.Body>
                    <Card.Title>{school.Nombre}</Card.Title>
                    <Card.Text>
                      Infraestructura: {school.Infraestructura} <br />
                      Preparación de Maestros: {school.Preparacion_Maestros} <br />
                      Acceso a Educación: {school.Acceso_Educacion} <br />
                      Finalización Básica: {school.Finalizacion_Basica} <br />
                      Finalización Media: {school.Finalizacion_Media} <br />
                      Mujeres con Acceso: {school.Mujeres_Acceso} <br />
                      Mujeres con Finalización: {school.Mujeres_Finalizacion} <br />
                      Acceso a Educación Superior: {school.Acceso_Superior}
                    </Card.Text>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </>
      )}
    </Container>
  );
}

export default FilterSchools;
