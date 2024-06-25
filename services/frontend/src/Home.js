import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

function Home() {
  return (
    <Container className="my-4">
      <Row>
        <Col>
          <Card className="text-center">
            <Card.Header as="h1">Bienvenido a la Página de Estadísticas de Colegios</Card.Header>
            <Card.Body>
              <Card.Text>
                En esta página puedes consultar diversas estadísticas sobre los colegios, filtrar por comuna, y ver las condiciones de infraestructura y preparación de los maestros.
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default Home;
