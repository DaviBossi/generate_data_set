# Pipeline de Geração do Dataset — Recorte de Imagens

Este pipeline é composto por dois scripts que trabalham em sequência para fatiar imagens grandes (heightmap + textura) em patches de 256×256 pixels, prontos para uso no treinamento do modelo Pix2Pix.

```
[generate_points.py]  →  points.txt  →  [cut_image.py]  →  patches do dataset
```

---

## Índice

1. [Visão Geral do Fluxo](#visão-geral-do-fluxo)
2. [Estrutura de Diretórios](#estrutura-de-diretórios)
3. [Passo 1 — Gerar os Pontos de Recorte](#passo-1--gerar-os-pontos-de-recorte)
4. [Passo 2 — Recortar as Imagens](#passo-2--recortar-as-imagens)
5. [Ajustando os Parâmetros](#ajustando-os-parâmetros)
6. [Adicionando Novos Pares de Imagens](#adicionando-novos-pares-de-imagens)

---

## Visão Geral do Fluxo

```
images/
├── height_map/height_map.png   ─┐
└── texture/tx_cortado.png       │
                                  ▼
                        [generate_points.py]
                                  │
                                  ▼
                   generate_data_set/src/points.txt
                   (lista de coordenadas x,y)
                                  │
                                  ▼
                         [cut_image.py]
                         /               \
            data-set/.../height_map/    data-set/.../texture/
            cut_image_0.png             cut_image_0.png
            cut_image_1.png             cut_image_1.png
            ...                         ...
```

> O mesmo arquivo `points.txt` é usado para recortar **ambas** as imagens, garantindo que cada patch de heightmap e seu patch de textura correspondente cubram exatamente a mesma região geográfica.

---

## Estrutura de Diretórios

Antes de executar os scripts, crie os diretórios de saída manualmente se ainda não existirem:

```
projeto/
│
├── images/
│   ├── height_map/
│   │   └── height_map.png        ← imagem de entrada do generate_points
│   └── texture/
│       └── tx_cortado.png        ← textura de entrada do cut_image
│
├── generate_data_set/
│   └── generate_data_set/
│       └── src/
│           └── points.txt        ← gerado automaticamente pelo generate_points
│
└── data-set/
    └── Hm_to_texture/
        ├── height_map/           ← patches de heightmap gerados pelo cut_image
        └── texture/              ← patches de textura gerados pelo cut_image
```

---

## Passo 1 — Gerar os Pontos de Recorte

**Script:** `generate_points.py`

Este script lê a imagem de referência, calcula uma grade de pontos de recorte com base no tamanho dela e salva as coordenadas em um arquivo `.txt`.

### Configuração

Abra `generate_points.py` e ajuste as duas variáveis no topo do arquivo:

```python
# Caminho para a imagem usada como referência de tamanho
image_input = "images/height_map/height_map.png"

# Diretório onde o arquivo points.txt será salvo
output_path = "generate_data_set/generate_data_set/src"
```

> Qualquer uma das duas imagens (heightmap ou textura) pode ser usada como referência, **desde que ambas tenham as mesmas dimensões**. O script só precisa do tamanho da imagem para calcular os pontos — ele não processa o conteúdo visual.

### Execução

```bash
python generate_points.py
```

**Saída esperada no console:**
```
Importing image...
Getting shape of the image...
Generating random points...
Saving points to file...
```

O arquivo `points.txt` será criado em `generate_data_set/generate_data_set/src/` com um par de coordenadas `x,y` por linha, como no exemplo abaixo:

```
0,0
32,0
64,0
...
```

---

## Passo 2 — Recortar as Imagens

**Script:** `cut_image.py`

Este script lê o `points.txt` gerado na etapa anterior e recorta tanto o heightmap quanto a textura em patches de **256×256 pixels**, salvando-os nos diretórios de saída.

### Configuração

Abra `cut_image.py` e ajuste as variáveis no topo:

```python
# Diretório raiz onde os patches serão salvos
# Os subdiretórios /texture e /height_map devem já existir dentro dele
output_path = "data-set/Hm_to_texture"
```

Em seguida, verifique os caminhos das imagens e do arquivo de pontos nas chamadas de importação:

```python
# Caminho para o arquivo de pontos gerado no Passo 1
texture_points = import_points("generate_data_set/generate_data_set/src/points.txt")

# Caminho para a textura a ser recortada
texture = import_image("images/texture/tx_cortado.png")

# Caminho para o heightmap a ser recortado
height_map = import_image("images/height_map/hm_cortado.png")
```

### Execução

```bash
python cut_image.py
```

**Saída esperada no console:**
```
Importando Pontos para a textura
Importando textura
Importando textura
Cortando textura em 256 pixels
Cutting images texture in pixels : 100%|████████| 2500/2500 [00:14<00:00]
Cortando height_map em 256 pixels
Cutting images height_map in pixels : 100%|████████| 2500/2500 [00:12<00:00]
```

Os patches serão nomeados sequencialmente (`cut_image_0.png`, `cut_image_1.png`, ...) e o índice `i` é o mesmo para heightmap e textura — ou seja, `height_map/cut_image_42.png` e `texture/cut_image_42.png` sempre correspondem à mesma região.

---

## Ajustando os Parâmetros

### Tamanho do tile (patch)

O tamanho padrão de cada patch é **256×256 pixels**, definido em dois lugares:

**Em `generate_points.py`** — controla o espaçamento da grade:
```python
points = grid_points(width, height, tile=256, stride=32)
#                                   ^^^^^^^^
```

**Em `cut_image.py`** — controla o tamanho real do recorte:
```python
box = (x, y, x + 256, y + 256)
#              ^^^^^    ^^^^^
```

> Ambos os valores devem ser alterados juntos para manter a consistência.

### Stride (passo entre os patches)

O `stride` em `grid_points` define o deslocamento em pixels entre um ponto de recorte e o próximo. O padrão é `32`.

```python
points = grid_points(width, height, tile=256, stride=32)
#                                             ^^^^^^^^^^
```

| Stride menor | Stride maior |
|---|---|
| Mais patches gerados | Menos patches gerados |
| Maior sobreposição entre patches | Menor sobreposição |
| Dataset maior, mais variado | Dataset menor, menos redundante |

Exemplo para um stride de 64 pixels (menos sobreposição):
```python
points = grid_points(width, height, tile=256, stride=64)
```

### Cobertura das bordas

O parâmetro `include_borders=True` garante que as bordas direita e inferior da imagem sempre sejam cobertas, mesmo que o stride não divida a imagem de forma exata. Para desativar:

```python
points = grid_points(width, height, tile=256, stride=32, include_borders=False)
```

---

## Adicionando Novos Pares de Imagens

Para gerar patches de um novo par heightmap/textura, siga os passos:

**1.** Aponte `image_input` em `generate_points.py` para a nova imagem de referência e execute o script para gerar um novo `points.txt`.

**2.** Atualize os caminhos em `cut_image.py`:

```python
texture_points = import_points("generate_data_set/generate_data_set/src/points.txt")
texture    = import_image("images/texture/nova_textura.png")
height_map = import_image("images/height_map/novo_heightmap.png")
```

**3.** Ajuste `output_path` para um diretório de saída diferente, evitando sobrescrever patches anteriores:

```python
output_path = "data-set/novo_lote"
# Crie os subdiretórios antes de executar:
# data-set/novo_lote/texture/
# data-set/novo_lote/height_map/
```

**4.** Execute `cut_image.py`.

**5.** Adicione o novo diretório ao `pairs` do script de treinamento Pix2Pix:

```python
pairs = [
    ...
    ("data-set/novo_lote/height_map", "data-set/novo_lote/texture"),
]
```
